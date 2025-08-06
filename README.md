# 🧠 Wordle Solver

A smart and user-friendly web application that helps players crack the daily NYT Wordle puzzle. It provides optimal word suggestions based on letter patterns and previous guess feedback.

---

## 🔍 Features

### 🔤 **Interactive Solver Interface**

- Enter 5-letter guesses using an intuitive UI
- Mark each letter based on Wordle’s feedback (⬛ Gray, 🟨 Yellow, 🟩 Green)
- Instantly view remaining valid word options
- Get intelligent next-word suggestions
- Track guess history in a dedicated sidebar
- Reset the game with a single click

### 📊 **Statistics & Visual Analysis**

- Letter frequency visualizations (overall and by position)
- Heatmaps and charts for in-depth letter insights
- Common word pattern analysis (e.g., CVCVC, CVCCV)
- Recommended starting words for better strategy
- Interactive graphs and visual data exploration

---

## 🛠️ Tech Stack

### 🧩 Backend

- Python 3
- Flask (web framework)
- Pandas (data manipulation & analysis)

### 🎨 Frontend

- HTML5 + CSS3
- JavaScript for interactivity
- Font Awesome for icons
- Inter font family
- Responsive, mobile-friendly layout

---

## 🚀 Getting Started

1. **Clone the Repository**

   ```bash
   git clone [repository-url]
   cd solver
   ```

2. **Install Dependencies**

   ```bash
   pip install flask pandas
   ```

3. **Run the App**

   ```bash
   python app.py
   ```

4. Open your browser and go to:

   ```
   http://localhost:5000
   ```

---

## 📁 Project Structure

```
solver/
├── app.py             # Main Flask app and route handling
├── solver.py          # Core solving logic and word filtering
├── word_ranking.csv   # Word frequency and ranking data
│
├── static/
│   ├── main.css       # Main application styling
│   ├── stats.css      # Stats dashboard styling
│   ├── app.js         # JavaScript for UI interaction
│   └── images/        # Pre-generated visualizations (optional)
│
└── templates/
    ├── index.html     # Main solver UI
    └── stats.html     # Statistics and insights page
```

---

## 🧑‍💻 Usage Guide

### 🎯 Solver Interface

1. **Enter Your Guess**

   - Use the input grid to type a valid 5-letter word

2. **Apply Wordle Feedback**

   - ⬛ **Gray**: Not in the word
   - 🟨 **Yellow**: In the word, wrong position
   - 🟩 **Green**: Correct position

3. **Explore Results**

   - View filtered list of possible answers
   - See the top suggested next guesses
   - All guesses are saved and shown in the sidebar
   - Use the reset button to start a new puzzle

---

## Next Steps!

### 📈 Statistics Dashboard

1. **Letter Frequency Analysis**

   - Displays how often each letter appears overall and in each position
   - Heatmap and bar graph visuals

2. **Word Pattern Insights**

   - Common patterns (e.g., consonant-vowel arrangements)
   - Frequency and success rate of each structure

3. **Best Starting Words**

   - Statistically optimized openers
   - Maximize letter coverage in early guesses
