from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from solver import WordleSolver

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages


try:
    # Load precomputed best start words DataFrame
    word_ranking_df = pd.read_csv("data/real_word_rankings.csv")
    real_words = word_ranking_df.loc[word_ranking_df["Is_Real"] == True]
    
except FileNotFoundError:
    print("Warning: word_ranking.csv not found, using default words")

# Initialize Wordle Solver
solver = WordleSolver()

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        # Initialize a list to store previous guesses if it doesn't already exist
        if "previous_guesses" not in session:
            session["previous_guesses"] = []
        if request.method == "POST":
            letters = []
            colors = []
            for i in range(5):
                letter = request.form.get(f'letter_{i}', '').strip().lower()
                color = request.form.get(f'color_{i}')
                letters.append(letter)
                colors.append(color)
            
            guess = ''.join(letters)
            if guess and len(guess) == 5:
                solver.update_constraints(guess, colors)
                letter_color_pairs = list(zip(guess, colors))  # Store letter + color
                session["previous_guesses"].append(letter_color_pairs)
                session.modified = True  # Save changes to session

        possible_words = sorted(solver.get_possible_words())
        ranked_words =  real_words[real_words["Word"].isin(possible_words)]
        ranked_words = ranked_words.sort_values(by="Final_Score", ascending=False).head(5)
        best_suggestions = ranked_words["Word"].tolist()

        return render_template(
            "index.html", 
            possible=possible_words, 
            suggestions=best_suggestions,
            previous_guesses=session["previous_guesses"])
        
    except Exception as e:
        print(f"Error in index route: {str(e)}")
        return render_template("index.html", 
                               possible=[], 
                               suggestions=[])

@app.route("/reset", methods=["POST"])
def reset():
    # Record game result before resetting
    success = len(solver.possible_words) == 1
    solver.end_game(success)
    solver.reset()
        # Clear previous guesses from the session
    if "previous_guesses" in session:
        session.pop("previous_guesses")
        
    return redirect(url_for('index'))

@app.route('/stats')
def stats():
    # solver_stats = solver.get_statistics()
    return render_template("stats.html")
    



if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Changed from default port 5000 to 5001

