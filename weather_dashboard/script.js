// ============================================
//   MOCK WEATHER DATA
//   (In real app you'd use an API like OpenWeatherMap)
// ============================================
const weatherData = {
    "london": {
        city: "London",
        country: "United Kingdom 🇬🇧",
        temp: 18,
        description: "Partly Cloudy",
        humidity: 65,
        wind: 12,
        visibility: 10,
        feelsLike: 15,
        icon: "⛅"
    },
    "new york": {
        city: "New York",
        country: "United States 🇺🇸",
        temp: 22,
        description: "Sunny",
        humidity: 55,
        wind: 8,
        visibility: 15,
        feelsLike: 20,
        icon: "☀️"
    },
    "tokyo": {
        city: "Tokyo",
        country: "Japan 🇯🇵",
        temp: 28,
        description: "Hot & Humid",
        humidity: 80,
        wind: 5,
        visibility: 8,
        feelsLike: 32,
        icon: "🌤️"
    },
    "paris": {
        city: "Paris",
        country: "France 🇫🇷",
        temp: 14,
        description: "Light Rain",
        humidity: 75,
        wind: 15,
        visibility: 6,
        feelsLike: 11,
        icon: "🌧️"
    },
    "dubai": {
        city: "Dubai",
        country: "UAE 🇦🇪",
        temp: 38,
        description: "Very Hot",
        humidity: 35,
        wind: 10,
        visibility: 12,
        feelsLike: 42,
        icon: "🌞"
    },
    "sydney": {
        city: "Sydney",
        country: "Australia 🇦🇺",
        temp: 25,
        description: "Clear Sky",
        humidity: 60,
        wind: 18,
        visibility: 20,
        feelsLike: 23,
        icon: "🌈"
    },
    "moscow": {
        city: "Moscow",
        country: "Russia 🇷🇺",
        temp: -5,
        description: "Heavy Snow",
        humidity: 85,
        wind: 20,
        visibility: 3,
        feelsLike: -12,
        icon: "❄️"
    },
    "mumbai": {
        city: "Mumbai",
        country: "India 🇮🇳",
        temp: 32,
        description: "Monsoon Rain",
        humidity: 90,
        wind: 25,
        visibility: 5,
        feelsLike: 38,
        icon: "⛈️"
    }
};

// Mock forecast data
const forecastData = [
    { day: "Mon", icon: "☀️", high: 20, low: 14 },
    { day: "Tue", icon: "⛅", high: 18, low: 12 },
    { day: "Wed", icon: "🌧️", high: 15, low: 10 },
    { day: "Thu", icon: "⛈️", high: 13, low: 9  },
    { day: "Fri", icon: "🌤️", high: 17, low: 11 }
];

// ============================================
//   STATE VARIABLES
// ============================================
let isFahrenheit = false;
let currentWeather = weatherData["london"];
let savedCities = [];
let notesTimer;

// ============================================
//   GET HTML ELEMENTS
// ============================================
const cityInput    = document.getElementById("city-input");
const searchBtn    = document.getElementById("search-btn");
const cityName     = document.getElementById("city-name");
const country      = document.getElementById("country");
const currentDate  = document.getElementById("current-date");
const weatherIcon  = document.getElementById("weather-icon");
const tempDisplay  = document.getElementById("temp");
const degreeUnit   = document.getElementById("degree-unit");
const description  = document.getElementById("description");
const humidity     = document.getElementById("humidity");
const wind         = document.getElementById("wind");
const visibility   = document.getElementById("visibility");
const feelsLike    = document.getElementById("feels-like");
const saveBtn      = document.getElementById("save-btn");
const savedList    = document.getElementById("saved-list");
const unitToggle   = document.getElementById("unit-toggle");
const forecastDiv  = document.getElementById("forecast");
const notes        = document.getElementById("notes");
const notesStatus  = document.getElementById("notes-status");
const clearNotes   = document.getElementById("clear-notes");

// ============================================
//   DISPLAY DATE FUNCTION
// ============================================
function displayDate() {
    const now = new Date();
    const options = {
        weekday: "long",
        year: "numeric",
        month: "short",
        day: "numeric"
    };
    currentDate.textContent = now.toLocaleDateString("en-US", options);
}

// ============================================
//   CELSIUS TO FAHRENHEIT
// ============================================
function celsiusToF(celsius) {
    return Math.round((celsius * 9/5) + 32);
}

// ============================================
//   DISPLAY WEATHER FUNCTION
// ============================================
function displayWeather(data) {
    currentWeather = data;

    // Update city info
    cityName.textContent = data.city;
    country.textContent = data.country;
    weatherIcon.textContent = data.icon;
    description.textContent = data.description;

    // Update temperature based on unit
    updateTemperature();

    // Update stats
    humidity.textContent    = data.humidity + "%";
    wind.textContent        = data.wind + " km/h";
    visibility.textContent  = data.visibility + " km";

    // Update date
    displayDate();

    // Update forecast
    displayForecast(data.temp);
}

// ============================================
//   UPDATE TEMPERATURE BASED ON UNIT
// ============================================
function updateTemperature() {
    if (isFahrenheit) {
        tempDisplay.textContent = celsiusToF(currentWeather.temp);
        feelsLike.textContent   = celsiusToF(currentWeather.feelsLike) + "°F";
        degreeUnit.textContent  = "°F";
    } else {
        tempDisplay.textContent = currentWeather.temp;
        feelsLike.textContent   = currentWeather.feelsLike + "°C";
        degreeUnit.textContent  = "°C";
    }
}

// ============================================
//   DISPLAY FORECAST
// ============================================
function displayForecast(baseTemp) {
    forecastDiv.innerHTML = "";

    forecastData.forEach((day, index) => {
        const variation = Math.floor(Math.random() * 6) - 3;
        const highTemp = baseTemp + variation;
        const lowTemp = highTemp - Math.floor(Math.random() * 6) - 2;

        const highDisplay = isFahrenheit ? celsiusToF(highTemp) : highTemp;
        const lowDisplay  = isFahrenheit ? celsiusToF(lowTemp) : lowTemp;
        const unit = isFahrenheit ? "°F" : "°C";

        const dayCard = document.createElement("div");
        dayCard.className = "forecast-day";
        dayCard.innerHTML = `
            <div class="day">${day.day}</div>
            <div class="f-icon">${day.icon}</div>
            <div class="f-temp">${highDisplay}${unit}</div>
            <div class="f-low">${lowDisplay}${unit}</div>
        `;
        forecastDiv.appendChild(dayCard);
    });
}

// ============================================
//   SEARCH CITY FUNCTION
// ============================================
function searchCity() {
    const input = cityInput.value.trim().toLowerCase();

    if (!input) {
        alert("Please enter a city name!");
        return;
    }

    if (weatherData[input]) {
        displayWeather(weatherData[input]);
        cityInput.value = "";
    } else {
        alert(`❌ City "${cityInput.value}" not found!\n\nTry: London, New York, Tokyo, Paris, Dubai, Sydney, Moscow, Mumbai`);
    }
}

// ============================================
//   CITY SELECT DROPDOWN
// ============================================

// Get the select element
const citySelect = document.getElementById("city-select");

// Listen for when user picks a city from dropdown
citySelect.addEventListener("change", () => {

    // Get the selected value
    const selectedCity = citySelect.value;

    // If they picked the placeholder "-- Select --"
    if (!selectedCity) return;

    // Find city in our data
    const data = weatherData[selectedCity];

    // Display weather for that city
    if (data) {
        displayWeather(data);

        // Reset dropdown back to placeholder
        // So user can select same city again
        citySelect.value = "";
    }
});

// ============================================
//   SAVE CITY FUNCTION (LOCAL STORAGE)
// ============================================
function saveCity() {
    const city = currentWeather.city;

    // Check if already saved
    if (savedCities.includes(city)) {
        alert(`${city} is already saved!`);
        return;
    }

    // Add to array
    savedCities.push(city);

    // Save to localStorage
    localStorage.setItem("savedCities", JSON.stringify(savedCities));

    // Update display
    renderSavedCities();

    alert(`✅ ${city} saved successfully!`);
}

// ============================================
//   RENDER SAVED CITIES LIST
// ============================================
function renderSavedCities() {
    savedList.innerHTML = "";

    if (savedCities.length === 0) {
        savedList.innerHTML = `
            <li style="color: rgba(255,255,255,0.3); font-size: 0.85rem; padding: 10px;">
                No saved cities yet
            </li>
        `;
        return;
    }

    savedCities.forEach((city, index) => {
        const li = document.createElement("li");
        li.className = "saved-city-item";
        li.innerHTML = `
            <span>🏙️ ${city}</span>
            <button class="delete-city" data-index="${index}">✕</button>
        `;

        // Click city name → load that city
        li.querySelector("span").addEventListener("click", () => {
            const data = weatherData[city.toLowerCase()];
            if (data) displayWeather(data);
        });

        // Click X → delete city
        li.querySelector(".delete-city").addEventListener("click", (e) => {
            e.stopPropagation();
            deleteCity(index);
        });

        savedList.appendChild(li);
    });
}

// ============================================
//   DELETE CITY FUNCTION
// ============================================
function deleteCity(index) {
    savedCities.splice(index, 1);
    localStorage.setItem("savedCities", JSON.stringify(savedCities));
    renderSavedCities();
}

// ============================================
//   LOAD FROM LOCAL STORAGE
// ============================================
function loadFromStorage() {
    // Load saved cities
    const stored = localStorage.getItem("savedCities");
    if (stored) {
        savedCities = JSON.parse(stored);
        renderSavedCities();
    } else {
        renderSavedCities();
    }

    // Load notes
    const storedNotes = localStorage.getItem("weatherNotes");
    if (storedNotes) {
        notes.value = storedNotes;
    }

    // Load unit preference
    const storedUnit = localStorage.getItem("unitPreference");
    if (storedUnit === "fahrenheit") {
        isFahrenheit = true;
        unitToggle.checked = true;
    }
}

// ============================================
//   NOTES AUTO-SAVE
// ============================================
notes.addEventListener("input", () => {
    notesStatus.textContent = "Saving...";

    // Clear previous timer
    clearTimeout(notesTimer);

    // Save after 1 second of no typing
    notesTimer = setTimeout(() => {
        localStorage.setItem("weatherNotes", notes.value);
        notesStatus.textContent = "✅ Saved!";

        setTimeout(() => {
            notesStatus.textContent = "Ready";
        }, 2000);
    }, 1000);
});

// ============================================
//   EVENT LISTENERS
// ============================================

// Search button
searchBtn.addEventListener("click", searchCity);

// Press Enter to search
cityInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") searchCity();
});

// Save button
saveBtn.addEventListener("click", saveCity);

// Unit toggle (°C / °F)
unitToggle.addEventListener("change", () => {
    isFahrenheit = unitToggle.checked;

    // Save preference
    localStorage.setItem(
        "unitPreference",
        isFahrenheit ? "fahrenheit" : "celsius"
    );

    // Update displayed temperatures
    updateTemperature();
    displayForecast(currentWeather.temp);
});

// Clear notes button
clearNotes.addEventListener("click", () => {
    if (confirm("Clear all notes?")) {
        notes.value = "";
        localStorage.removeItem("weatherNotes");
        notesStatus.textContent = "Cleared";
    }
});

// ============================================
//   INITIALIZE APP
// ============================================
loadFromStorage();          // Load saved data
displayWeather(weatherData["london"]);  // Show default city