from django.db import models

# Create your models here.
class AST(models.Model):
    type = models.CharField(max_length=15)
    left = models.ForeignKey('self', blank=True, on_delete=models.CASCADE, related_name='LeftChild', null=True)
    right = models.ForeignKey('self', blank=True, on_delete=models.CASCADE, related_name='RightChild', null=True)
    operator = models.CharField(max_length=5, blank=True, null=True)
    left_operand = models.CharField(max_length=100, blank=True, null=True)
    condition = models.CharField(max_length=3, blank=True, null=True)
    right_operand = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        if self.type == 'operator':
            return self.operator
        else:
            return f'{self.left_operand} {self.condition} {self.right_operand}'

class Rule(models.Model):
    rule_name = models.CharField(max_length=100, unique=True)
    rule_ast = models.ForeignKey(AST, blank=True, on_delete=models.CASCADE, related_name='Rule')
    rule = models.CharField(max_length=1024, default='None')
    def __str__(self) -> str:
        return self.rule_name