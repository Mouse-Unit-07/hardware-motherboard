import re
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

LOG_FILE = "drift-test.log"


# -----------------------------------------------------------------------------
# parsing
# -----------------------------------------------------------------------------
def parse_log(filename):
    text = Path(filename).read_text(errors="ignore")

    target_match = re.search(
        r"encoder target for each run:\s*(-?\d+)",
        text,
        re.IGNORECASE
    )

    if not target_match:
        raise RuntimeError("Could not find encoder target")

    encoder_target = abs(int(target_match.group(1)))

    #
    # Full dataset (for tables)
    #
    all_datasets = {
        ("forward", "enc1"): [],
        ("forward", "enc2"): [],
        ("backward", "enc1"): [],
        ("backward", "enc2"): [],
    }

    #
    # Trimmed dataset (for fitting/plots)
    #
    fit_datasets = {
        ("forward", "enc1"): [],
        ("forward", "enc2"): [],
        ("backward", "enc1"): [],
        ("backward", "enc2"): [],
    }

    started = {
        ("forward", "enc1"): False,
        ("forward", "enc2"): False,
        ("backward", "enc1"): False,
        ("backward", "enc2"): False,
    }

    direction = None
    current_speed = None

    for line in text.splitlines():

        if "moving motors forward" in line:
            direction = "forward"
            continue

        if "moving motors backward" in line:
            direction = "backward"
            continue

        speed_match = re.search(r"speed:\s*(-?\d+)", line)

        if speed_match:
            current_speed = int(speed_match.group(1))
            continue

        encoder_match = re.search(
            r"enc1=(-?\d+),\s*enc2=(-?\d+)",
            line
        )

        if encoder_match and direction is not None and current_speed is not None:

            enc1 = int(encoder_match.group(1))
            enc2 = int(encoder_match.group(2))

            drift1 = abs(enc1) - encoder_target
            drift2 = abs(enc2) - encoder_target

            key1 = (direction, "enc1")
            key2 = (direction, "enc2")

            #
            # Save ALL data for tables
            #
            all_datasets[key1].append((current_speed, drift1))
            all_datasets[key2].append((current_speed, drift2))

            #
            # Remove initial encoder==0 region only
            # for fitting dataset
            #
            if abs(enc1) > 0:
                started[key1] = True

            if abs(enc2) > 0:
                started[key2] = True

            if started[key1]:
                fit_datasets[key1].append((current_speed, drift1))

            if started[key2]:
                fit_datasets[key2].append((current_speed, drift2))

    return all_datasets, fit_datasets, encoder_target


# -----------------------------------------------------------------------------
# fitting
# -----------------------------------------------------------------------------
def r_squared(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)

    if ss_tot == 0:
        return 1.0

    return 1 - ss_res / ss_tot


def fit_linear(x, y):

    coeffs = np.polyfit(x, y, 1)

    m = coeffs[0]
    b = coeffs[1]

    y_fit = m * x + b

    return {
        "name": "linear",
        "r2": r_squared(y, y_fit),
        "y_fit": y_fit,
        "equation": f"y = {m:.6f}x + {b:.6f}"
    }


def fit_exponential(x, y):

    #
    # exponential fit requires positive values
    #
    shift = 0

    if np.min(y) <= 0:
        shift = abs(np.min(y)) + 1
        y_shifted = y + shift
    else:
        y_shifted = y.copy()

    log_y = np.log(y_shifted)

    coeffs = np.polyfit(x, log_y, 1)

    b = coeffs[0]
    ln_a = coeffs[1]

    a = np.exp(ln_a)

    y_fit_shifted = a * np.exp(b * x)
    y_fit = y_fit_shifted - shift

    return {
        "name": "exponential",
        "r2": r_squared(y, y_fit),
        "y_fit": y_fit,
        "equation":
            f"y = {a:.6f} * exp({b:.6f}x)"
            + (f" - {shift}" if shift else "")
    }


def best_fit(x, y):

    linear = fit_linear(x, y)

    try:
        exponential = fit_exponential(x, y)

        if exponential["r2"] > linear["r2"]:
            return exponential

    except Exception:
        pass

    return linear


# -----------------------------------------------------------------------------
# plotting
# -----------------------------------------------------------------------------
def create_plot(title, x, y):

    fit = best_fit(x, y)

    x_line = np.linspace(np.min(x), np.max(x), 500)

    if fit["name"] == "linear":

        m, b = np.polyfit(x, y, 1)
        y_line = m * x_line + b

    else:

        y_min = np.min(y)

        shift = abs(y_min) + 1 if y_min <= 0 else 0

        log_y = np.log(y + shift)

        coeffs = np.polyfit(x, log_y, 1)

        b_exp = coeffs[0]
        a_exp = np.exp(coeffs[1])

        y_line = a_exp * np.exp(b_exp * x_line) - shift

    plt.figure(figsize=(10, 6))

    plt.scatter(x, y, label="Measured Drift")
    plt.plot(x_line, y_line, linewidth=2, label="Best Fit")

    plt.title(
        f"{title}\n"
        f"{fit['equation']}\n"
        f"R² = {fit['r2']:.6f}"
    )

    plt.xlabel("Speed")
    plt.ylabel("Encoder Drift (ticks)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    safe_name = title.lower().replace(" ", "_")
    plt.savefig(f"{safe_name}.png", dpi=300)

    print()
    print(title)
    print("Model :", fit["name"])
    print("Fit   :", fit["equation"])
    print("R²    :", fit["r2"])

# -----------------------------------------------------------------------------
# table
# -----------------------------------------------------------------------------
def print_table(direction, all_datasets):

    enc1 = dict(all_datasets[(direction, "enc1")])
    enc2 = dict(all_datasets[(direction, "enc2")])

    speeds = sorted(
        set(enc1.keys()) |
        set(enc2.keys())
    )

    print()
    print("=" * 70)
    print(f"{direction.upper()} DRIFT TABLE")
    print("(drift = abs(encoder reading) - encoder target)")
    print("=" * 70)

    print(
        f"{'Speed':>8} | "
        f"{'ENC1 Drift':>12} | "
        f"{'ENC2 Drift':>12}"
    )

    print("-" * 70)

    for speed in speeds:

        drift1 = enc1.get(speed, "")
        drift2 = enc2.get(speed, "")

        print(
            f"{speed:>8} | "
            f"{drift1:>12} | "
            f"{drift2:>12}"
        )

# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
all_datasets, datasets, target = parse_log(LOG_FILE)

print(f"Encoder target = {target}")

print_table("forward", all_datasets)
print_table("backward", all_datasets)

for direction in ["forward", "backward"]:
    for encoder in ["enc1", "enc2"]:

        data = datasets[(direction, encoder)]

        if not data:
            continue

        speeds = np.array([d[0] for d in data], dtype=float)
        drift = np.array([d[1] for d in data], dtype=float)

        create_plot(
            f"{encoder.upper()} {direction.capitalize()}",
            speeds,
            drift
        )

plt.show()
