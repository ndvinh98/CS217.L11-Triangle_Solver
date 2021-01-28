from odoo.models import Model

# from odoo.exceptions import UserError


def show_result(self, goals):
    rs = []
    for g in goals:
        print("{}: {} -> {}".format(g[1][0], g[1][2], " ".join(g[1][1])))
        rs.append("{}: {} -> {}".format(g[1][0], g[1][2], " ".join(g[1][1])))
    return rs


def check_validation(self, GT, KL):
    if any(item in GT for item in KL):
        print("Invalid KL set")
        return False
    return True


def forward_chainning(self, rules, GT, KL):
    if not check_validation(self, GT, KL):
        return
    is_found_rule = False
    is_found_solution = True
    facts = GT
    goals = []
    while len(rules) > 0:
        for key, value in rules.items():
            if any(item not in facts for item in key):
                is_found_rule = False
                continue
            else:
                # Nếu kết quả suy ra từ VP có trong tập facts thì loại rule này
                if all(elem in facts for elem in value[1]):
                    rules.pop(key)
                    is_found_rule = True
                    break

                # Ngược lại thêm rule vào tâp goal và pop khỏi tập rules
                list_facts = list(facts)
                list_facts.extend(value[1])
                facts = set(list_facts)
                goals.append([key, value])
                if value[1] == KL:
                    return goals
                rules.pop(key)
                is_found_rule = True
                break
        if not is_found_rule:
            is_found_solution = False
            break

    if any(k not in facts for k in KL):
        is_found_solution = False
    if is_found_solution:
        return goals
    return False


def filter_duplicated_rules(self, rules):
    current_destination_rules = []
    filter_rules = []
    if rules:
        for rule in rules:
            if rule[1][1] not in current_destination_rules:
                current_destination_rules.append(rule[1][1])
                filter_rules.append(rule)
            else:
                continue
        return filter_rules


def compact_answer(self, goals, GT):
    goals = filter_duplicated_rules(self, goals)
    is_finish = False

    while not is_finish and len(goals) > 1:
        for i in range(0, len(goals) - 1):
            goal_keys = [goal[0] for goal in goals]
            # flatten
            goal_keys = {item for items in goal_keys for item in items}
            if all(
                destination_rule not in goal_keys for destination_rule in goals[i][1][1]
            ):
                goals.pop(i)
                is_finish = False
                break
            else:
                is_finish = True
                continue

        if is_finish:
            break

    return goals


Model.show_result = show_result
Model.check_validation = check_validation
Model.forward_chainning = forward_chainning
Model.filter_duplicated_rules = filter_duplicated_rules
Model.compact_answer = compact_answer
