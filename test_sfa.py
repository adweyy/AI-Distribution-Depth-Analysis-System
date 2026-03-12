import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fabric_connector import _run_dax_sfa

print("Fetching table list from SFA dataset...")

dax = 'EVALUATE SELECTCOLUMNS(INFO.TABLES(), "TableName", [Name])'
df = _run_dax_sfa(dax)
print(df.to_string())