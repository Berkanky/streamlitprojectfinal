import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
#use_container_width=True

dosya=pd.read_csv("fortune.csv")
dosya=dosya.drop(columns=["permalink"])
st.title("FORTUNE 500 COMPANIES")
lists=dosya.set_index("sector")
sectors=lists.index
sectors=list(sectors.unique())
sectorst=st.multiselect("Choose Sectors",sectors,default=sectors[0:21])
if sectorst:
    dosya=lists.loc[sectorst]
reven = dosya["revenues"]
minreven = min(reven)
maxreven = max(reven)
profits=dosya["profits"]
minprofits=min(profits)
maxprofits=max(profits)
employees=dosya["employees"]
minemployees=min(employees)
maxemployees=max(employees)
col1, col2 = st.columns(2)
with col2:
    revensec = st.slider("Min Revenue", minreven, maxreven)
    profitssec=st.slider("Min Profit",minprofits,maxprofits)
    employeessec=st.slider("Min Employee",minemployees,maxemployees)
    if revensec:
        dosya = dosya[dosya["revenues"] >= revensec]
    if profitssec:
        dosya=dosya[dosya["profits"]>=profitssec]
    if employeessec:
        dosya=dosya[dosya["employees"]>=employeessec]
with col1:
    dosya=dosya.reset_index()
    st.dataframe(dosya)
    @st.cache
    def convert_df(dosya):
        return dosya.to_csv().encode('utf-8')
csv = convert_df(dosya)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Fortune500.csv',
    mime='text/csv',
)

newdf=pd.read_csv("fortune.csv")
newdf=newdf[["rank","year","name","sector","industry","profits","hqcity","profitable","ceowoman","jobgrowth"]]
@st.cache
def sirketfiltre(sirketad):
    sirketbul=newdf[newdf["name"].str.contains(sirketad)]
    return sirketbul
rank=newdf["rank"]
minrank=int(min(rank))
maxrank=int(max(rank))
year=newdf["year"]
minyear=min(year)
maxyear=max(year)
col1,col2=st.columns(2)
with col1:
    sirketisim=st.text_input("Enter Company Name")
    newdf=sirketfiltre(sirketisim)
    ranksec=st.slider("Min Rank",minrank,maxrank)
    yearsec=st.number_input("Year",minyear,maxyear,value=2021)
    gendersec=st.checkbox("Gender(Default=All)")
    profitablesec=st.checkbox("Profitable (Default=All)")
    jobgrowthst=st.checkbox("JobGrowth (Default=All)")
            #ınd=newdf.set_index("industry")
            #ınds=ınd.index
            #ınds=list(ınds.unique())
            #ındustryst=st.multiselect("Enter Name Of Industry",ınds)
            #if ındustryst:
                #newdf=ınd.loc[ındustryst]
                #newdf=newdf.reset_index()
    if profitablesec:
        newdf=newdf[newdf["profitable"]=="no"]
        st.write("Only NoN Profitable")
    if gendersec:
        newdf=newdf[newdf["ceowoman"]=="yes"]
        st.write("Only CEO Woman")
    if ranksec:
        newdf=newdf[newdf["rank"]>=ranksec]
    if yearsec:
        newdf=newdf[newdf["year"]==yearsec]
    if jobgrowthst:
        newdf=newdf[newdf["jobgrowth"]=="no"]
        st.write("Only NoN Jobgrowth")
with col2:
    st.dataframe(newdf)
    @st.cache
    def convert_df(newdf):
        return newdf.to_csv().encode('utf-8')
csv = convert_df(newdf)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Fortune500.csv',
    mime='text/csv',
)
df=pd.read_csv("fortune.csv")
df["revchange"]=df["revchange"].fillna(0)
df["prftchange"]=df["prftchange"].fillna(0)
df=df.drop(columns=["hqstate","permalink"])
col1,col2=st.columns(2)
with col1:
    dfcolumns=["sector","industry","hqcity"]
    stfirst=st.selectbox("Select First Column",dfcolumns)
with col2:
    dfcolumns2=["revenues","revchange","profits","prftchange","assets","employees"]
    stsecond=st.selectbox("Select Second Column",dfcolumns2)
with col2:
    dfyear=list(df["year"].unique())
    dfyear.insert(0,"All Years")
    dfyearst=st.selectbox("Select Year",dfyear)
    if dfyearst!="All Years":
        df=df[df["year"]==dfyearst]
df=df.groupby(stfirst)[stsecond].mean()
df=df.reset_index()
df=df.sort_values(by=[stsecond],ascending=False)
graphlist=["Pie Graph","Bar Graph"]
with col1:
    graphst=st.selectbox("Select Graph",graphlist)
if graphst=="Pie Graph":
    fig=px.pie(df,values=stsecond,names=stfirst,title=stfirst,height=650)
if graphst=="Bar Graph":
    fig=px.bar(df,x=stfirst,y=stsecond,title=stfirst)
st.plotly_chart(fig,use_container_width=True)
#st.dataframe(df)
