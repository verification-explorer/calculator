"""Demo file for learning the Debug Console."""


def calculate_sum(numbers):
    """Calculate sum of a list - good for debugging practice."""
    total = 0
    for i, num in enumerate(numbers):
        total = total + num
        print(f"Step {i}: total = {total}")
    return total


def main():
    numbers = [10, 20, 30, 40, 50]
    message = "Calculating sum..."
    print(message)

    result = calculate_sum(numbers)

    doubled = result * 2
    print(f"Sum: {result}, Doubled: {doubled}")


if __name__ == "__main__":
    main()
