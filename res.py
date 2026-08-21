from flask import Flask, render_template, request
from inference_engine import forward_chaining

import os
import re


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# IMAGE DIRECTORY
# =========================================================

IMAGE_FOLDER = os.path.join(
    app.static_folder,
    "images"
)


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text):
    """
    Converts restaurant names into a common format.

    Example:

    Domino's Pizza
        ↓
    dominospizza

    Dominos_Pizza
        ↓
    dominospizza
    """

    if not text:
        return ""

    text = str(text).lower()

    # Remove file extension if present
    text = os.path.splitext(text)[0]

    # Keep only letters and numbers
    text = re.sub(r"[^a-z0-9]", "", text)

    return text


# =========================================================
# FIND RESTAURANT IMAGE
# =========================================================

def find_restaurant_image(restaurant):

    restaurant_name = restaurant.get(
        "name",
        ""
    )

    location = restaurant.get(
        "location",
        ""
    )


    # Normalize restaurant information

    normalized_name = normalize_text(
        restaurant_name
    )

    normalized_location = normalize_text(
        location
    )


    # If image folder does not exist

    if not os.path.exists(IMAGE_FOLDER):

        print("Image folder not found!")

        return None


    # Get all files

    image_files = os.listdir(
        IMAGE_FOLDER
    )


    # =====================================================
    # FIRST METHOD
    # Exact restaurant + location matching
    # =====================================================

    for filename in image_files:

        # Only image files

        if not filename.lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp")
        ):

            continue


        normalized_filename = normalize_text(
            filename
        )


        # Example:

        # Restaurant:
        # Domino's Pizza
        #
        # Location:
        # Chennai
        #
        # File:
        # 010_Chennai_Dominos_Pizza.jpg
        #
        # Normalized:
        # dominospizza
        # chennai
        # 010chennaidominospizza


        if (
            normalized_name in normalized_filename
            and normalized_location in normalized_filename
        ):

            print(
                f"Image matched: "
                f"{restaurant_name} -> {filename}"
            )

            return filename


    # =====================================================
    # SECOND METHOD
    # Restaurant name only
    # =====================================================

    for filename in image_files:

        if not filename.lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp")
        ):

            continue


        normalized_filename = normalize_text(
            filename
        )


        if normalized_name in normalized_filename:

            print(
                f"Image matched by name: "
                f"{restaurant_name} -> {filename}"
            )

            return filename


    # =====================================================
    # NO IMAGE FOUND
    # =====================================================

    print(
        f"No image found for: "
        f"{restaurant_name} ({location})"
    )

    return None


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# RECOMMENDATION ROUTE
# =========================================================

@app.route(
    "/recommend",
    methods=["POST"]
)
def recommend():

    # =====================================================
    # GET USER INPUT
    # =====================================================

    cuisine = request.form.get(
        "cuisine",
        ""
    ).strip()


    budget = request.form.get(
        "budget",
        ""
    ).strip()


    veg = request.form.get(
        "veg",
        ""
    ).strip()


    group = request.form.get(
        "group",
        ""
    ).strip()


    location = request.form.get(
        "location",
        ""
    ).strip()


    # =====================================================
    # CREATE USER INPUT
    # =====================================================

    user_input = {

        "cuisine": cuisine,

        "budget": budget,

        "veg": veg,

        "group": group,

        "location": location

    }


    # =====================================================
    # RUN INFERENCE ENGINE
    # =====================================================

    recommendations = forward_chaining(
        user_input
    )


    # =====================================================
    # FIND IMAGE FOR EVERY RESTAURANT
    # =====================================================

    for item in recommendations:

        restaurant = item["restaurant"]


        image_filename = find_restaurant_image(
            restaurant
        )


        # Add image information

        restaurant["image"] = image_filename


    # =====================================================
    # DISPLAY RESULT PAGE
    # =====================================================

    return render_template(
        "result.html",

        recommendations=recommendations,

        user_input=user_input
    )


# =========================================================
# RUN FLASK
# =========================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "             DINEWISE AI"
    )

    print(
        "   RESTAURANT RECOMMENDATION SYSTEM"
    )

    print("=" * 60)

    print(
        f"Images folder: {IMAGE_FOLDER}"
    )

    app.run(
        debug=True
    )