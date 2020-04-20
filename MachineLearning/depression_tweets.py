import twint

c = twint.Config()

c.Search = "#depression"
c.Limit = 8000
c.Format = "id: {id} | tweet: {tweet}"
c.Store_csv = True
c.Output = "depression.csv"
c.Lang = "en"

twint.run.Search(c)