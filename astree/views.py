import re
from django.shortcuts import render
from astree.models import AST, Rule

# Create your views here.

def home(request):
    return render(request, 'home.html')

def ListAllRules(request):
    return render(request, 'allRules.html', {'rules':Rule.objects.all()})

def create_rule(type, operator=None, left_operand=None, condition=None, right_operand=None):
    newRule, created = AST.objects.get_or_create(
        type=type,
        operator=operator,
        left_operand=left_operand,
        condition=condition,
        right_operand=right_operand,
    )
    return newRule

def InfixToPrefix(rule):
    equalities = ['<','>','=','!=']
    operators = ['AND', 'OR']
    tokens = re.findall(r"\(|\)|AND|OR|>|<|=|!=|\w+|'.+?'", rule)
    stack = []
    prefix = []
    tokenLen = len(tokens)
    i = 0
    while i < tokenLen:
        if tokens[i] in equalities:
            operand = prefix.pop()
            newS = create_rule('operand', None, operand.strip("'"), tokens[i].strip("'"), tokens[i+1].strip("'"))
            prefix.append(newS)
            i += 1
        elif tokens[i] in operators:
            stack.append(tokens[i])
        elif tokens[i] == '(':
            stack.append(tokens[i])
        elif tokens[i] == ')':
            while stack and stack[-1]!= '(':
                prefix.append(stack.pop())
            stack.pop()
        else:
            prefix.append(tokens[i])
        i += 1
    prefix.extend(stack)
    return prefix

def combine_rules(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        rule = request.POST.get('rule')
        operators = ['AND', 'OR']
        stack = []
        try:
            prefix = InfixToPrefix(rule)
        except IndexError as e:
            return render(request, "createRule.html", {'error': 'Your RULE has some mistake in Brackets or Operators.' })
        except Exception as e:
            return render(request, "createRule.html", {'error': str(e)})
        try:
            for word in prefix:
                if word in operators:
                    op1 = stack.pop()
                    op2 = stack.pop()
                    try:
                        new_node = AST.objects.create(type='operator', operator=word)
                    except Exception as e:
                        return render(request, "createRule.html", {'error': str(e)})
                    new_node.left = op1
                    new_node.right = op2
                    new_node.save()
                    stack.append(new_node)
                else:
                    stack.append(word)
        except IndexError as e:
            return render(request, "createRule.html", {'error': 'Your RULE has some mistake in Brackets or Operators.' })
        except Exception as e:
            return render(request, "createRule.html", {'error': str(e)})
        try:
            newRule = Rule.objects.get_or_create(
                rule_name = name,
                rule_ast = stack.pop(),
                rule = rule,
            )
        except Exception as e:
            return render(request, "createRule.html", {'error': str(e)})
        return render(request, "createRule.html", {'status': True, 'rule': rule})
    return render(request, "createRule.html")

def evaluate(node, data):
    if node.type == 'operator':
        left_result = evaluate(node.left, data)
        right_result = evaluate(node.right, data)
        if node.operator == 'AND':
            return left_result and right_result
        elif node.operator == 'OR':
            return left_result or right_result
    elif node.type == 'operand':
        # Get the value from the data and compare it
        user_value = data.get(node.left_operand)
        if node.condition == '>':
            return int(user_value) > int(node.right_operand)
        elif node.condition == '<':
            return int(user_value) < int(node.right_operand)
        elif node.condition == '=':
            return str(user_value) == node.right_operand
        # Add more comparison operators as needed
    return False
def evaluate_rule(request):
    names =  Rule.objects.all()
    if request.method == 'POST':
        rule_name = request.POST.get('rule')
        try:
            node = Rule.objects.get(rule_name=rule_name)
        except Exception as e:
            return render(request, 'evaluation.html', {'error': str(e), 'names': names})
        data = eval(request.POST.get('data'))
        value = evaluate(node.rule_ast, data)
        return render(request, 'evaluation.html', {'rule_name':rule_name, 'data':data, 'value':value, 'names': names})
    return render(request, 'evaluation.html', {'names': names})