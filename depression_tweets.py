import twint

c = twint.Config()

c.Search = "depression"
c.Limit = 10
c.Store_csv = True
c.Output = "test.csv"
c.Lang = "en"

twint.run.Search(c)