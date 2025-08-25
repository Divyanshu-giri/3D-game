from config import *

class CraftingSystem:
    def __init__(self):
        self.inventory = {resource: 0 for resource in RESOURCE_TYPES.keys()}
        self.crafted_items = []

    def add_resource(self, resource_type, amount):
        if resource_type in self.inventory:
            self.inventory[resource_type] += amount

    def open_crafting_menu(self):
        print("Crafting Menu:")
        for item, recipe in CRAFTING_RECIPES.items():
            can_craft = True
            for resource, amount in recipe.items():
                if self.inventory.get(resource, 0) < amount:
                    can_craft = False
                    break
            print(f"{item}: {recipe} - {'Craftable' if can_craft else 'Not enough resources'}")

    def craft_item(self, item_name):
        if item_name in CRAFTING_RECIPES:
            recipe = CRAFTING_RECIPES[item_name]
            # Check if enough resources
            for resource, amount in recipe.items():
                if self.inventory.get(resource, 0) < amount:
                    print(f"Not enough {resource} to craft {item_name}")
                    return False
            
            # Deduct resources
            for resource, amount in recipe.items():
                self.inventory[resource] -= amount
            
            # Add crafted item
            self.crafted_items.append(item_name)
            print(f"Crafted {item_name} successfully!")
            return True
        else:
            print(f"Unknown item: {item_name}")
            return False

    def get_inventory(self):
        return self.inventory

    def get_crafted_items(self):
        return self.crafted_items
