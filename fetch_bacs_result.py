import pandas as pd
from urllib.request import Request, urlopen


def fetch_res(uni_name, url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    df = pd.read_html(webpage)[0]
    col_name = df.columns 
    score = [str(i) for i in df[col_name[2]]]
    name = df[col_name[1]]
    df_in = df[col_name[0]]
    df_score = []
    df_penalty = [] 
    df_name = []
    df_pos = []
    now = 0
    for i in name :
        if i.find(uni_name) is not -1:
            if df_in[now] < 175 :
                df_score.append(score[now][:3])
                df_penalty.append(score[now][3:])
            elif df_in[now] < 294 : 
                df_score.append(score[now][:2])
                df_penalty.append(score[now][2:])
            else : 
                df_score.append(score[now][:1])
                df_penalty.append(score[now][1:])
            
            df_pos.append(str(df_in[now]))
            df_name.append(name[now][:name[now].find('[')-1])
        now+=1
    new_df = pd.DataFrame()
    new_df['Position'] = df_pos
    new_df['Name'] = df_name
    new_df['Score'] = df_score
    new_df['Penalty'] = df_penalty
    return new_df
    
def main():
    uni_name = 'IIUC'
    url = 'https://algo.codemarshal.org/contests/bacsrpc18/standings?page='
    df_lst = []
    for i in range(7) : df_lst.append(fetch_res (uni_name, url+str(i+1)))
    final_df = pd.concat(df_lst)
    final_df.to_csv('BACS_Standings_only_'+uni_name+'.csv', index=False)

if __name__ == '__main__':
    main()
