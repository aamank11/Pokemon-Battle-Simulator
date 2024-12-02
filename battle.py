import math
import project
from flask import Flask, render_template, request, jsonify


def compare_hp(pkmn1, pkmn2): 
    if project.get_hp(pkmn1) >= project.get_hp(pkmn2):
        return pkmn1
    else:
        return pkmn2
    

def compare_speed(pkmn1, pkmn2):
    if project.get_speed(pkmn1) > project.get_speed(pkmn2):
        return pkmn1
    elif project.get_speed(pkmn1) < project.get_speed(pkmn2):
        return pkmn2
    else:
        return "Draw"


def get_num_types(pkmn):
    if project.get_type2(pkmn) != "DNE":
        return 2
    else:
        return 1


def same_region(pkmn1, pkmn2): 
    if project.get_region(pkmn1) == project.get_region(pkmn2):
        return True
    return False


def damage(attacker, defender):
    physical_damage = 10 * project.get_attack(attacker) / project.get_defense(defender)
    special_damage = 10 * project.get_special_attack(attacker) / project.get_special_defense(defender)
    if physical_damage >= special_damage:
        return physical_damage
    else:
        return special_damage


def type_bonus(attack_type, defender):
    defender_type1 = project.get_type1(defender)
    defender_type2 = project.get_type2(defender)
    if project.get_type2(defender) == "DNE":
        bonus = project.get_type_effectiveness(attack_type, defender_type1)
        return bonus
    else:
        bonus = project.get_type_effectiveness(attack_type, defender_type1) * project.get_type_effectiveness(attack_type, defender_type2)
        return bonus


def effective_damage(attacker, defender):
    if get_num_types(attacker) == 2:
        if type_bonus(project.get_type1(attacker), defender) >= type_bonus(project.get_type2(attacker), defender):
            return type_bonus(project.get_type1(attacker), defender) * damage(attacker, defender)
        else:
            return type_bonus(project.get_type2(attacker), defender) * damage(attacker, defender)
    else:
        return type_bonus(project.get_type1(attacker), defender) * damage(attacker, defender)


def num_hits(attacker, defender):
    eff_dam = effective_damage(attacker, defender)
    if round(eff_dam, 4) == 0:
        return "infinitely many"
    else:
        return math.ceil(project.get_hp(defender)/eff_dam)


def battle(pkmn1, pkmn2):
    if num_hits(pkmn1, pkmn2) > num_hits(pkmn2, pkmn1):
        return pkmn2
    elif num_hits(pkmn1, pkmn2) == num_hits(pkmn2, pkmn1):
        return compare_speed(pkmn1, pkmn2)
    else:
        return pkmn1
    

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/battle", methods=["POST"])
def battle_endpoint():
    data = request.get_json()
    pkmn1 = data["pkmn1"].capitalize()
    pkmn2 = data["pkmn2"].capitalize()
    winner = battle(pkmn1, pkmn2)
    return jsonify({"winner": winner})

if __name__ == "__main__":
    app.run(debug=True)










