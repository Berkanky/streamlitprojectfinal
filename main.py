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
fig=px.bar(newdf,x=newdf["sector"],y=newdf["profits"])
st.plotly_chart(fig,use_container_width=True)
