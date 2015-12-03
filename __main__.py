"main入口"
print('__main__.py imported:', __name__)



import os.path
import sys
sys.argv[0] = __file__
COC_fol = os.path.dirname(os.path.abspath(__file__))
COC_dir = os.path.dirname(COC_fol)
sys.path.insert(0, COC_fol)
# sys.path.insert(0, COC_dir)

import Clan_py3
Clan_py3.main()
