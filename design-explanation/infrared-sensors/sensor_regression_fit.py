#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt


ADC_TO_VOLTAGE_SCALE = 9.0 / 3520.0

# Distance where model switches
PIECEWISE_SPLIT_DISTANCE = 4.0


def adc_reading_to_voltage(adc_reading):
    return adc_reading * ADC_TO_VOLTAGE_SCALE


def parse_input_file(filename):
    distances = []
    voltages = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            distance_str, adc_str = line.split()

            distance = float(distance_str)
            adc_reading = float(adc_str)

            voltage = adc_reading_to_voltage(adc_reading)

            distances.append(distance)
            voltages.append(voltage)

    return distances, voltages


def split_dataset(x_values, y_values, split_distance):
    near_x = []
    near_y = []

    far_x = []
    far_y = []

    for x, y in zip(x_values, y_values):
        if x <= split_distance:
            near_x.append(x)
            near_y.append(y)
        else:
            far_x.append(x)
            far_y.append(y)

    return near_x, near_y, far_x, far_y


def linear_regression(x_values, y_values):
    n = len(x_values)

    sum_x = sum(x_values)
    sum_y = sum(y_values)

    sum_xx = sum(x * x for x in x_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))

    denominator = (n * sum_xx) - (sum_x * sum_x)

    m = ((n * sum_xy) - (sum_x * sum_y)) / denominator

    b = (sum_y - (m * sum_x)) / n

    return m, b


def inverse_regression(x_values, y_values):
    transformed_x = [1.0 / x for x in x_values]

    return linear_regression(transformed_x, y_values)


def predict_near(m, b, x):
    return (m * x) + b


def predict_far(a, b, x):
    return (a / x) + b


def piecewise_predict(split_distance,
                      near_m,
                      near_b,
                      far_a,
                      far_b,
                      x):
    if x <= split_distance:
        return predict_near(near_m, near_b, x)

    return predict_far(far_a, far_b, x)


def compute_r_squared(x_values,
                      y_values,
                      split_distance,
                      near_m,
                      near_b,
                      far_a,
                      far_b):
    predictions = [
        piecewise_predict(
            split_distance,
            near_m,
            near_b,
            far_a,
            far_b,
            x
        )
        for x in x_values
    ]

    mean_y = sum(y_values) / len(y_values)

    ss_res = sum(
        (y - y_pred) ** 2
        for y, y_pred in zip(y_values, predictions)
    )

    ss_tot = sum(
        (y - mean_y) ** 2
        for y in y_values
    )

    return 1.0 - (ss_res / ss_tot)


def generate_piecewise_curve(split_distance,
                             near_m,
                             near_b,
                             far_a,
                             far_b,
                             min_x,
                             max_x,
                             points=400):
    curve_x = []
    curve_y = []

    step = (max_x - min_x) / (points - 1)

    for i in range(points):
        x = min_x + (i * step)

        y = piecewise_predict(
            split_distance,
            near_m,
            near_b,
            far_a,
            far_b,
            x
        )

        curve_x.append(x)
        curve_y.append(y)

    return curve_x, curve_y


def plot_results(raw_x, raw_y, curve_x, curve_y):
    plt.figure()

    plt.scatter(raw_x, raw_y, label="Measured Data")
    plt.plot(curve_x, curve_y, label="Piecewise Best Fit")

    plt.xlabel("Distance (cm)")
    plt.ylabel("Sensor Output Voltage (V)")
    plt.title("IR Sensor Distance vs Voltage")

    plt.grid(True)
    plt.legend()

    plt.show()


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <data_file>")
        sys.exit(1)

    filename = sys.argv[1]

    distances, voltages = parse_input_file(filename)

    near_x, near_y, far_x, far_y = split_dataset(
        distances,
        voltages,
        PIECEWISE_SPLIT_DISTANCE
    )

    near_m, near_b = linear_regression(
        near_x,
        near_y
    )

    far_a, far_b = inverse_regression(
        far_x,
        far_y
    )

    r_squared = compute_r_squared(
        distances,
        voltages,
        PIECEWISE_SPLIT_DISTANCE,
        near_m,
        near_b,
        far_a,
        far_b
    )

    print("Piecewise regression model:")
    print()

    print(f"For distance <= {PIECEWISE_SPLIT_DISTANCE:.2f} cm:")
    print(f"V(distance) = ({near_m:.8f} * distance) + {near_b:.8f}")
    print()

    print(f"For distance > {PIECEWISE_SPLIT_DISTANCE:.2f} cm:")
    print(f"V(distance) = ({far_a:.8f} / distance) + {far_b:.8f}")
    print()

    print(f"Overall R^2 = {r_squared:.8f}")

    curve_x, curve_y = generate_piecewise_curve(
        PIECEWISE_SPLIT_DISTANCE,
        near_m,
        near_b,
        far_a,
        far_b,
        min(distances),
        max(distances)
    )

    plot_results(
        distances,
        voltages,
        curve_x,
        curve_y
    )


if __name__ == "__main__":
    main()