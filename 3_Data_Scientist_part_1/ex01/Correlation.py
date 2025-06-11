import pandas as pd

def main():
	df = pd.read_csv("../data/Train_knight.csv")
	df.columns = df.columns.str.strip()
	df["knight"] = df["knight"].map({"Jedi": 1, "Sith": 0})

	features = [col for col in df.columns]
	corr = df[features].corrwith(df["knight"]).sort_values(ascending=False)

	for feature, value in corr.items():
		print(f"{feature:15} {value:>15.6f}")

if __name__ == "__main__":
	main()