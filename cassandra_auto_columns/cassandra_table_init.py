import os.path
import pandas as pd

if __name__ == "__main__":
    columns_list = pd.read_csv("tfidf_feature_list.csv", header=None)
    columns_list = columns_list.T

    columns_list = columns_list.rename(columns={0: 'words'})

    if not os.path.exists("1_init_keyspace.cql"):
        f = open("1_init_keyspace.cql", "x")

    if not os.path.exists("2_init_columnfamily.cql"):
        f = open("2_init_columnfamily.cql", "x")

    with open("1_init_keyspace.cql", "w") as f:
        f.write("CREATE KEYSPACE IF NOT EXISTS caffeine\n  WITH REPLICATION = {\n   'class' : 'SimpleStrategy',\n   'replication_factor' : 2\n};")

    with open("2_init_columnfamily.cql", "w") as f:
        f.write("CREATE COLUMNFAMILY caffeine.new_caffeine (\n  drink_name text PRIMARY KEY,\n  volume float,\n  calories float,\n  caffeine_ml float, \n  caffeine_over_ml float,")
        f.write("\n   ")
        for c in columns_list["words"]:
            tmp = str(c)
            tmp = tmp.replace(" ","_")
            f.write(f"\n  {tmp} float,")
        f.write("\n);")
