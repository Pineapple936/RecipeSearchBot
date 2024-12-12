import sqlite3

def about_dish(dish_id: int) -> dict:
    """
    Getting information about the dish by its ID number.

    Args:
        dish_id (int): ID number of the dish.

    Returns:
        dict: Information about the dish.
    """
    connect = sqlite3.connect("database/Dish.db")
    cursor = connect.cursor()
    dish = dict()

    main_info = cursor.execute("SELECT title, calories, count_portions, cooking FROM Dish WHERE id = ?;", (dish_id, )).fetchone()
    dish["title"] = main_info[0]
    dish["calories"] = main_info[1]
    dish["count_portions"] = main_info[2]
    dish["cooking"] = main_info[3]

    dish["product"] = list()
    dish["amount"] = list()
    for product in cursor.execute("SELECT products, amount FROM Product WHERE dish_id = ?", (dish_id, )).fetchall():
        dish["product"].append(product[0])
        dish["amount"].append(product[1])

    dish["recipe"] = cursor.execute("SELECT recipe FROM Recipe WHERE dish_id = ?", (dish_id, )).fetchone()

    return dish

def search_recipes(products: str) -> list[dict]:
    """
    Search for a recipe for a dish by products.

    Args:
        products (str): List of products (separated by commas).

    Returns:
        list[dict]: The search result with the response code and content.
    """
    connect = sqlite3.connect("database/Dish.db")
    cursor = connect.cursor()
    products = products.lower().split(",")
    products = [products[i].strip() for i in range(len(products))if products[i] != ""]
    dishes = dict()

    for product in products:
        query = f"SELECT dish_id FROM Product WHERE products GLOB '*{product}*'"
        cursor.execute(query)
        ids = [id[0] for id in cursor.fetchall()]

        for id in ids:
            if id not in dishes:
                dishes[id] = 1
            else:
                dishes[id] += 1

    connect.close()

    if len(dishes) != 0:
        keys = [[key, dishes[key]] for key in dishes]
        keys.sort(key = lambda x: x[1])
        recipes = [about_dish(key[0]) for key in keys]
        return {"responce": 200, "content": recipes}
    return {"responce": 0, "content": "К сожалению, я не нашел рецептов по этим ингридиентам. Попробуйте другие продукты"}

def create_message(dish: dict) -> str:
    """
    Create a message with information about a dish based on a list of products.

    If the dish is found, a message with a detailed description of the recipe is returned.
    Otherwise, a message is returned stating that the recipe is unknown.

    Args:
        dish (dict): Dictionary with dish data.

    Returns:
        str: A message with a description of the dish or a message about the absence of a recipe.
    """
    message = dish["title"] + "\n\n" + "Продукты:\n"

    for i in range(len(dish["product"])):
        message += f"• {dish['product'][i]} {dish['amount'][i]}\n"

    message += "\n" + "Процесс приготовления:\n"

    for line in dish["recipe"]:
        message += line

    message += "\n" + f"В одной порции {dish['calories']}\n" + f"Время приготовления: {dish['cooking']}\nКоличество порций: {dish['count_portions']}"

    return message
