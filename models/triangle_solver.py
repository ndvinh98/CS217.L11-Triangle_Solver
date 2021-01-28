import logging

# from . import forward_chainning
from odoo import fields, models
from odoo.exceptions import UserError
import math

_logger = logging.getLogger(__name__)

TRIANGLE_PARAMS = [
    ("side", "Cạnh"),
    ("angle", "Góc"),
    ("height", "Đường cao"),
    ("inscribed_circle", "Bán kính đường tròn nội tiếp"),
    ("circumscribed_cirlce", "Bán kính đường tròn ngoại tiếp"),
    ("perimeter", "Chu vi"),
    ("half_perimeter", "Nửa chu vi"),
    ("aria", "Diện tích"),
]


class TriangleParameter(models.Model):
    _name = "triangle.parametter"
    _description = "Triangle Parametters"

    name = fields.Char(string="Name", readonly=True)
    value = fields.Float(string="Value")
    type = fields.Selection(selection=TRIANGLE_PARAMS, readonly=True)


class TriangleRule(models.Model):
    _name = "triangle.rule"
    _description = "Triangle Rules"

    name = fields.Char(string="Rule id")
    rule_hypothesis_variables = fields.Many2many(
        string="Hypothesis variables",
        comodel_name="triangle.parametter",
        relation="triangle_rule_hypothesis_variable_rel",
    )
    rule_conclution_variable = fields.Many2one(
        string="Conclution variable", comodel_name="triangle.parametter"
    )
    equation = fields.Char(string="Equation")


class TriangleProblem(models.Model):
    _name = "triangle.problem"
    _description = "Triangle Problems"

    name = fields.Char(string="Problem name")
    rule_ids = fields.Many2many(
        string="Rules applied",
        comodel_name="triangle.rule",
        relation="triangle_problem_rule_rel",
        readonly=True,
    )
    problem_hypothesis_variables = fields.Many2many(
        string="Hypothesis variables",
        comodel_name="triangle.parametter",
        relation="triangle_problem_hypothesis_variable_rel",
    )
    problem_conclution_variable = fields.Many2one(
        string="Conclution variable", comodel_name="triangle.parametter"
    )
    notes = fields.Text("Information", readonly=True)

    def solve_problem(self):

        hypothesis_set = set(self.problem_hypothesis_variables.mapped("name"))
        conclution_value = [self.problem_conclution_variable.name]
        rules = self.convert_rules()

        result = self.forward_chainning(rules, hypothesis_set, conclution_value)
        if not result:
            raise UserError("Not found solution !!!")
        compact_result = self.compact_answer(result, hypothesis_set)
        self.calculate_conclution_variable(compact_result)

    def convert_rules(self):
        """
            ('B','C') : [ 'f1', ['A'] , 'A=180-B-C' ]
            Rule được convert sang dạng key value như trên

            key ('B', 'C') : tập giả thiết của luật
            value: [ 'f1', ['A'] , 'A=180-B-C' ]

                trong đó 'f1' : tên rule
                        ['A'] : Tập kết luận
                        A=180-B-C' : công thức để suy ra luật
        """
        list_rule = {}
        for rule_id in self.rule_ids:
            key = tuple(rule_id.rule_hypothesis_variables.mapped("name"))
            value = [
                rule_id.name,
                [rule_id.rule_conclution_variable.name],
                rule_id.equation,
            ]

            list_rule.update(
                {key: value,}
            )
        return list_rule

    def calculate_conclution_variable(self, result):
        all_params = self.env["triangle.parametter"].search([])
        A = all_params.filtered(lambda p: p.name == "A").mapped("value")[0]
        B = all_params.filtered(lambda p: p.name == "B").mapped("value")[0]
        C = all_params.filtered(lambda p: p.name == "C").mapped("value")[0]
        a = all_params.filtered(lambda p: p.name == "a").mapped("value")[0]
        b = all_params.filtered(lambda p: p.name == "b").mapped("value")[0]
        c = all_params.filtered(lambda p: p.name == "c").mapped("value")[0]
        ha = all_params.filtered(lambda p: p.name == "ha").mapped("value")[0]
        hb = all_params.filtered(lambda p: p.name == "hb").mapped("value")[0]
        hc = all_params.filtered(lambda p: p.name == "hc").mapped("value")[0]
        p = all_params.filtered(lambda p: p.name == "p").mapped("value")[0]
        r = all_params.filtered(lambda p: p.name == "r").mapped("value")[0]
        S = all_params.filtered(lambda p: p.name == "S").mapped("value")[0]

        solution = "Found solution !!! \n"
        for res in result:
            if res[1][0] == "f1":
                C = 180 - A - B
                rs = C
            if res[1][0] == "f2":
                B = 180 - A - C
                rs = B
            if res[1][0] == "f3":
                A = 180 - B - C
                rs = A
            if res[1][0] == "f4":
                a = math.sqrt(
                    pow(b, 2) + pow(c, 2) - 2 * b * c * math.cos(math.radians(A))
                )
                rs = a
            if res[1][0] == "f5":
                b = math.sqrt(
                    pow(a, 2) + pow(c, 2) - 2 * a * c * math.cos(math.radians(B))
                )
                rs = b
            if res[1][0] == "f6":
                c = math.sqrt(
                    pow(a, 2) + pow(b, 2) - 2 * a * b * math.cos(math.radians(C))
                )
                rs = c
            if res[1][0] == "f7":
                p = (a + b + c) / 2
                rs = p
            if res[1][0] == "f8":
                S = a * ha / 2
                rs = S
            if res[1][0] == "f9":
                S = b * hb / 2
                rs = S
            if res[1][0] == "f10":
                S = c * hc / 2
                rs = S
            if res[1][0] == "f11":
                S = p * r
                rs = S
            if res[1][0] == "f12":
                S = math.sqrt(p * (p - a) * (p - b) * (p - c))
                rs = S
            if res[1][0] == "f13":
                ha = b * math.sin(math.radians(C))
                rs = ha
            if res[1][0] == "f14":
                hb = a * math.sin(math.radians(C))
                rs = hb
            if res[1][0] == "f15":
                hc = a * math.sin(math.radians(B))
                rs = hc

            solution += "{} : {} => {} = {}\n".format(
                res[1][0], res[1][2], res[1][1][0], rs
            )

        raise UserError(str(solution))
