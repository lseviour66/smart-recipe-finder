import streamlit as st
from api import search_by_ingredients, get_meal_details

st.set_page_config(page_title="Smart Recipe Finder", layout="wide")

# --- CSS ---
st.markdown("""
<style>

.recipe-card {
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    border-radius: 10px;
    padding: 6px;
}
.recipe-card:hover {
    transform: scale(1.03);
    box-shadow: 0 0 18px rgba(255, 200, 0, 0.55);
}

.recipe-title {
    font-size: 0.85rem;
    font-weight: 600;
    text-align: center;
    margin-top: 4px;
}

.view-text {
    font-size: 0.75rem;
    color: #555;
    text-align: center;
}

.right-pane {
    margin-top: -10px !important;
}

</style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("Smart Recipe Finder 🍳")
st.write("Tell me what's in your fridge and I'll find recipes for you.")

# --- Ingredient input ---
ingredients_input = st.text_input("Enter ingredients (comma separated):")

user_ingredients = []
results = []

if ingredients_input:
    user_ingredients = [i.strip().lower() for i in ingredients_input.split(",")]
    results = search_by_ingredients(user_ingredients)

# --- Determine if a recipe is open ---
recipe_open = "selected_meal" in st.session_state

# --- Layout ---
if recipe_open:
    left_col, right_col = st.columns([0.45, 0.55])
else:
    left_col = st.container()
    right_col = None

# ------------------------------------------------------------
# LEFT PANE — Recipe list (always visible)
# ------------------------------------------------------------
with left_col:
    if ingredients_input:
        st.subheader(f"Found {len(results)} recipes")

        cols = st.columns(4)
        idx = 0

        for meal in results:
            with cols[idx]:
                st.markdown("<div class='recipe-card'>", unsafe_allow_html=True)

                # CLICKABLE IMAGE — no button box, no navigation
                with st.form(key=f"form_{meal['idMeal']}"):
                    st.image(meal["strMealThumb"], use_container_width=True)
                    submitted = st.form_submit_button("View")
                    if submitted:
                        st.session_state["selected_meal"] = meal["idMeal"]
                        st.rerun()

                # Title + View Recipe text
                st.markdown(
                    f"""
                    <div class='recipe-title'>{meal['strMeal']}</div>
                    
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("</div>", unsafe_allow_html=True)

            idx = (idx + 1) % 4

# ------------------------------------------------------------
# RIGHT PANE — Recipe details
# ------------------------------------------------------------
if right_col and recipe_open:
    with right_col:
        st.markdown("<div class='right-pane'>", unsafe_allow_html=True)

        meal = get_meal_details(st.session_state["selected_meal"])

        # Close button
        if st.button("← Close Recipe"):
            del st.session_state["selected_meal"]
            st.rerun()

        st.header(meal["strMeal"])
        st.image(meal["strMealThumb"], width=350)

        # Extract ingredients
        recipe_ingredients = []
        for i in range(1, 21):
            ing = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")
            if ing and ing.strip():
                recipe_ingredients.append((ing.lower(), measure))

        # Classify have vs missing
        missing = []
        have = []
        for ing, measure in recipe_ingredients:
            if ing in user_ingredients:
                have.append((ing, measure))
            else:
                missing.append((ing, measure))

        st.subheader("Ingredients Check")

        st.markdown("### You already have:")
        for ing, measure in have:
            st.checkbox(f"{ing.capitalize()} — {measure}", value=True, disabled=True)

        st.markdown("### You might need:")
        for ing, measure in missing:
            st.checkbox(f"{ing.capitalize()} — {measure}")

        st.subheader("Instructions")
        st.write(meal["strInstructions"])

        if meal.get("strSource"):
            st.subheader("Recipe Website")
            st.components.v1.iframe(meal["strSource"], height=600)

