import requests
import json

weather_api_key = '722eee1249e64f4ea31163850240801'

def fetch_weather_data(city):
    url = f'https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}'
    try:
        response = requests.get(url)
        return response.json()
    except requests.RequestException as error:
        print(f"Error fetching weather data: {error}")
        return None

def main_menu():
    while True:
        print('-------------------')
        print('1. Check Weather')
        print('2. Add to Favorites')
        print('3. Show Favorites')
        print('4. Quit')
        print('-------------------')

        choice = input('Enter the number: ')

        if choice == '1':
            city_input = input('Enter city name: ') or 'chennai'
            weather_data = fetch_weather_data(city_input)

            if weather_data and 'current' in weather_data:
                temperature = weather_data['current'].get('temp_c')
                if temperature is not None:
                    print(f'{city_input}: {temperature} °C')
                else:
                    print(f"No temperature information available for {city_input}")
            else:
                print(f"No weather data available for {city_input}")
        elif choice == '2':
            add_to_favorites()
        elif choice == '3':
            show_favorite_cities()
        elif choice == '4':
            print('Thank you for using the weather app!')
            break
        else:
            print('Invalid input')

def add_to_favorites():
    while True:
        city_input = input('Enter city name or "n" to exit: ')
        with open('favorites.json', 'r') as file:
            fav_data = json.load(file)

        existing_favorites = fav_data.get('cities', [])

        if city_input.lower() == 'n':
            break
        elif city_input and not city_input.isdigit() and city_input not in existing_favorites:
            existing_favorites.append(city_input)
            fav_data['cities'] = existing_favorites

            with open('favorites.json', 'w') as file:
                json.dump(fav_data, file, indent=4)

            print('City added to favorites')
        elif not city_input:
            print("Please enter a valid city name!")
        elif city_input.isdigit():
            print("Please enter a valid city name, not a number!")
        else:
            print("City already exists in favorites")

def show_favorite_cities():
    while True:
        with open('favorites.json', 'r') as file:
            fav_data = json.load(file)
            favorite_cities = fav_data.get('cities', [])
            
            if favorite_cities:
                print("Your favorite cities:")
                for i, city in enumerate(favorite_cities, start=1):
                    print(f"{i}. {city}")

                action_choice = input('Choose an action:\n1. Update a city\n2. Delete a city\n3. Exit\nEnter the number: ')

                if action_choice == '1':
                    update_city(favorite_cities, fav_data)
                elif action_choice == '2':
                    delete_city(favorite_cities)
                elif action_choice == '3':
                    break
                else:
                    print('Invalid input.')
            else:
                print("You haven't added any cities to your favorites yet.")

def delete_city(favorite_cities):
    remove_input = input('Enter the number of the city to remove: ')
    try:
        city_index = int(remove_input) - 1
        if 0 <= city_index < len(favorite_cities):
            removed_city = favorite_cities.pop(city_index)
            with open('favorites.json', 'w') as file:
                json.dump({"cities": favorite_cities}, file, indent=2)
            print(f"'{removed_city}' removed from favorites.")
        else:
            print("Invalid number. No changes made to favorites.")
    except ValueError:
        print("Invalid input. No changes made to favorites.")

def update_city(favorite_cities, fav_data):
    update_input = input('Enter the number of the city to update: ')
    try:
        city_index = int(update_input) - 1
        if 0 <= city_index < len(favorite_cities):
            new_city_name = input("Enter the updated city name: ")
            favorite_cities[city_index] = new_city_name
            fav_data['cities'] = favorite_cities

            with open('favorites.json', 'w') as file:
                json.dump(fav_data, file, indent=2)

            print(f"City updated to '{new_city_name}'.")
        else:
            print("Invalid number. No changes made to favorites.")
    except ValueError:
        print("Invalid input. No changes made to favorites.")

if __name__ == "__main__":
    main_menu()
