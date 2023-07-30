import requests
import json

# Function to fetch weather information from OpenWeatherMap API


def get_weather_info(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=API_KEY&units=metric"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

# Function to print weather information


def print_weather_info(city):
    data = get_weather_info(city)
    if data["cod"] == "404":
        print("City not found.")
        return
    weather_desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    print(f"Current weather in {city}: {weather_desc}")
    print(f"Temperature: {temp}°C")
    print(f"Feels like: {feels_like}°C")
    print(f"Humidity: {humidity}%")
    print(f"Wind speed: {wind_speed} m/s")

# Function to convert temperature from Celsius to Fahrenheit


def celsius_to_fahrenheit(temp_celsius):
    return (temp_celsius * 9/5) + 32

# Function to convert temperature from Fahrenheit to Celsius


def fahrenheit_to_celsius(temp_fahrenheit):
    return (temp_fahrenheit - 32) * 5/9

# Function to check if a given year is a leap year


def is_leap_year(year):
    if year % 4 != 0:
        return False
    elif year % 100 != 0:
        return True
    elif year % 400 != 0:
        return False
    else:
        return True

# Function to calculate the factorial of a number


def factorial(num):
    if num == 0:
        return 1
    else:
        return num * factorial(num - 1)

# Function to calculate the nth Fibonacci number


def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)


# Main program loop
while True:
    print("Choose an option:")
    print("1. Get weather information for a city")
    print("2. Convert temperature from Celsius to Fahrenheit")
    print("3. Convert temperature from Fahrenheit to Celsius")
    print("4. Check if a year is a leap year")
    print("5. Calculate the factorial of a number")
    print("6. Calculate the nth Fibonacci number")
    print("7. Quit")

    option = input("Enter your choice: ")

    if option == "1":
        city = input("Enter the city name: ")
        print_weather_info(city)
    elif option == "2":
        temp_celsius = float(input("Enter the temperature in Celsius: "))
        temp_fahrenheit = celsius_to_fahrenheit(temp_celsius)
        print(f"{temp_celsius}°C = {temp_fahrenheit}°F")
    elif option == "3":
        temp_fahrenheit = float(input("Enter the temperature in Fahrenheit: "))
        temp_celsius = fahrenheit_to_celsius(temp_fahrenheit)
        print(f"{temp_fahrenheit}°F = {temp_celsius}°C")
    elif option == "4":
        print("Please enter the word to be searched:")
    search_word = input().lower()
    search_result = search_word_occurrences(search_word, file_content)
    if search_result:
        print(
            f"The word '{search_word}' was found {len(search_result)} times in the file.")
        print("The occurrences are:")
        for line_number, line_content in search_result:
            print(f"Line {line_number}: {line_content}")
    else:
        print(f"The word '{search_word}' was not found in the file.")

    elif option == "5":
    print("Please enter the word to be replaced:")
    search_word = input().lower()
    print("Please enter the replacement word:")
    replace_word = input()
    replace_count = replace_word_occurrences(
        search_word, replace_word, file_path)
    print(f"{replace_count} occurrences of the word '{search_word}' were replaced with '{replace_word}' in the file.")

    elif option == "6":
        print("Please enter the word to be added:")
        add_word = input()
        add_to_file(add_word, file_path)
        print(f"The word '{add_word}' was added to the file.")

    elif option == "7":
        print("Please enter the word to be removed:")
        remove_word = input().lower()
        remove_count = remove_word_occurrences(remove_word, file_path)
        print(f"{remove_count} occurrences of the word '{remove_word}' were removed from the file.")

    elif option == "8":
        print("Exiting program...")
        exit()

else:
    print("Invalid option. Please choose again.")
