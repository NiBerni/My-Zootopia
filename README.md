# My Zootopia - Animal Web Generator 🐾

*This project was created as part of my journey to becoming a Back-End Engineer
at [masterschool.com](https://www.masterschool.com).*

A dynamic Python command-line application that fetches animal data via a REST API and generates a beautiful, filterable
HTML showcase.

## 🌟 Features

* **Live API Integration:** Retrieves up-to-date animal characteristics using the API-Ninjas Animals API.
* **Smart Search & Filtering:** Search for specific animals (e.g., "fox", "bear") and filter the results further by
  attributes like diet, location, or skin type.
* **HTML Generation:** Automatically parses the data and builds a clean, responsive HTML file to view in your browser.
* **OOP Architecture:** Built with a strong focus on Object-Oriented Programming, utilizing reusable data models and
  repository patterns.

## 🛠️ Prerequisites

* Python 3.9+
* An active API Key from [API-Ninjas](https://api-ninjas.com/api/animals)

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/NiBerni/My-Zootopia.git](https://github.com/yourusername/My-Zootopia.git)
   cd My-Zootopia

2. **Install dependecies:**
    ```bash
    pip install -r requirements.txt
3. **Configure the Environment**

Create a `.env` file in the root directory and add your API key:

    API_KEY=your_api_ninjas_key_here
    API_URL=[https://api.api-ninjas.com/v1/animals](https://api.api-ninjas.com/v1/animals)

## 💻 Usage

Run the application:

```bash
python animals_web_generator.py
```

**Follow the interactive prompts:**

* Enter the name of an animal you want to look up.
* Choose if and how you want to filter the results.
* Open the newly generated animal_page.html in your favorite web browser.

(Pro Tip: Try searching for a non-existent animal to trigger our special 404 easter egg!)

## 📁 Project Structure

* animals_web_generator.py: Main CLI script handling user input and page generation.
* animal_class.py: Defines the AnimalModel and its HTML rendering logic.
* external_classes/: Git submodule containing base structures like BaseDataModel and the ApiRepository.
* animals_template.html: The base HTML/CSS blueprint used for generation.