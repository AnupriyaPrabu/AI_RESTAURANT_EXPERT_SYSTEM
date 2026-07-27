from inference_engine import forward_chaining


def main():

    print("=" * 60)
    print("         AI RESTAURANT EXPERT SYSTEM")
    print("=" * 60)

    cuisine = input("Enter Cuisine: ")
    budget = input("Enter Budget (Low/Medium/High): ")
    veg = input("Veg? (Yes/No): ")
    group = input("Enter Group Size (Solo/Couple/Small Group/Family Group/Large Group): ")
    location = input("Enter Location (Chennai/Bangalore/Hyderabad/Kochi): ")

    user_input = {
        "cuisine": cuisine,
        "budget": budget,
        "veg": veg,
        "group": group,
        "location": location
    }

    recommendations = forward_chaining(user_input)

    print("\n" + "=" * 60)

    if recommendations:

        print("Top Restaurant Recommendations\n")

        for i, item in enumerate(recommendations, start=1):

            restaurant = item["restaurant"]
            score = item["score"]
            matched_rules = item["matched_rules"]
            explanation = item["explanation"]

            print(f"{i}. {restaurant['name']}")
            print(f"   Match Score : {score}/12")

            print("\n   Rules Fired:")

            for rule in matched_rules:
                print(f"      ✓ {rule} Matched")

            print(f"\n   Reason      : {explanation}")

            print(f"   Cuisine     : {restaurant['cuisine']}")
            print(f"   Budget      : {restaurant['budget']}")
            print(f"   Veg         : {restaurant['veg']}")
            print(f"   Group       : {restaurant['group']}")
            print(f"   Location    : {restaurant['location']}")

            print("-" * 60)

    else:
        print("Sorry! No suitable restaurants found.")

    print("=" * 60)


if __name__ == "__main__":
    main()