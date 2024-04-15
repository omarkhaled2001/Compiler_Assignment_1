from Regex2Postfix import Shunting_Yard, validate_Regex
from Postfix2NFA import NFA

def main():
    cases0 = '''
    (AB)
    (A|B) 
    ([A-Z])
    (A+)
    (A*)
    (((AB)((A|B)*))(AB))
    (A(((B*)|(DA))*))((CG)|(D([DEF])))
    (ab
    (a([b-c))
    ((a|b)|)  
    (a{3,2})
    ((((AB)|[X-Z])+)([C-F]*))
    (((((ABE)|C)|((([A-C])S)*))+)((AB)C))  
    ((([a-e_])(([a-c0-3_])*))(([!?])?))
    '''
    cases1 = {0: 'ab(b|c)*d+', 1: ' (AB)', 2: '(A|B)', 3: '([A-Z])', 4: '(A)+', 5: '(A)*', 6: '(((AB)((A|B)*))(AB))', 7: '((((AB)|[A-Z])+)([A-Z]*))', 8: '(((((ABE)|C)|((([A-Z])S)*))+)((AB)C))',
             9: '((([a-z_])(([a-z0-9_])*))(([!?])?))', 10: '(A(((B*)|(DA))*))((CG)|(D([DEF])))', 11: '(ab', 12: '(a([b-c))', 13: '((a|b)|)', 14: '(a{3,2})'}
    regex = '(AB)'

    # regex = input("Enter regular expression: ")
    if not validate_Regex(regex):
        return
    try:
        postfix = Shunting_Yard(regex)
        print("----------------------------------------------------------------")
        print("regex:", regex)
        print("----------------------------------------------------------------")
        print("postfix: ", postfix)
        print("----------------------------------------------------------------")
        NFA_obj = NFA(postfix=postfix)
        print("NFA: ", NFA_obj.NFA_JSON_Converter())
        NFA_obj.NFA_Graph(name='output/NFA.gv', view=False)
        print("----------------------------------------------------------------")
    # catch the exception and print it
    except Exception as e:
        print(e)
        print("Your Regex is invalid")

if __name__ == '__main__':
    main()
