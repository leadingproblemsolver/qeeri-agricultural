import json,sys
from qeeri_brain import ask,verify_receipts,evaluate_case,last_receipt
if __name__=='__main__':
    if len(sys.argv)<2:
        print('Usage: python cli.py ask "Qatar cucumber imports 2024" | case OBS-WITS-2024 | verify');sys.exit(2)
    kind=sys.argv[1]
    try:
        if kind=='ask': result=ask(' '.join(sys.argv[2:]))
        elif kind=='case':result=evaluate_case(sys.argv[2])
        elif kind=='verify':result=verify_receipts()
        elif kind=='last':result=last_receipt()
        else:raise ValueError('Unknown command')
        print(json.dumps(result,indent=2))
    except (ValueError,IndexError) as e:
        print(str(e),file=sys.stderr);sys.exit(2)
