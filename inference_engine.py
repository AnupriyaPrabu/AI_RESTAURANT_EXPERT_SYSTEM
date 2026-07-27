from knowledge_base import restaurants
from rules import rules


def forward_chaining(user_input):

    recommendations = []

    # Check if all required inputs are provided
    for condition in rules[0]["conditions"]:
        if condition not in user_input or user_input[condition].strip() == "":
            return []

    # Normalize user input
    cuisine = user_input["cuisine"].strip().lower()
    budget = user_input["budget"].strip().lower()
    veg = user_input["veg"].strip().lower()
    group = user_input["group"].strip().lower()
    location = user_input["location"].strip().lower()

    # Check each restaurant
    for restaurant in restaurants:

        # ----------------------------
        # Rule 1 : Location
        # ----------------------------
        if restaurant["location"].strip().lower() != location:
            continue

        score = 0
        matched_rules = []

        # Location rule fired
        matched_rules.append("Location")

        # ----------------------------
        # Rule 2 : Cuisine
        # ----------------------------
        if restaurant["cuisine"].strip().lower() == cuisine:
            score += 5
            matched_rules.append("Cuisine")

        # ----------------------------
        # Rule 3 : Budget
        # ----------------------------
        if restaurant["budget"].strip().lower() == budget:
            score += 3
            matched_rules.append("Budget")

        # ----------------------------
        # Rule 4 : Veg Preference
        # ----------------------------
        if restaurant["veg"].strip().lower() == veg:
            score += 2
            matched_rules.append("Veg Preference")

        # ----------------------------
        # Rule 5 : Group Size
        # ----------------------------
        if restaurant["group"].strip().lower() == group:
            score += 2
            matched_rules.append("Group Size")

        # ----------------------------
        # Generate Explanation
        # ----------------------------
        if score == 12:
            explanation = "Perfect match for all your preferences."
        elif score >= 9:
            explanation = "Matches most of your preferences."
        elif score >= 6:
            explanation = "Matches several of your preferences."
        elif score >= 5:
            explanation = "Basic match for your preferences."
        else:
            explanation = "Not recommended."

        # ----------------------------
        # Minimum Score Rule
        # ----------------------------
        if score >= 5:

            recommendations.append({
                "restaurant": restaurant,
                "score": score,
                "matched_rules": matched_rules,
                "explanation": explanation
            })

    # Sort restaurants by score
    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # Return Top 3
    return recommendations[:3]