import requests
from bs4 import BeautifulSoup
import streamlit as st
import pickle
import numpy as np
import pandas as pd

model = pickle.load(open('ORFmodel.pkl', 'rb'))

def calculate_credibility_score(ratings, num_of_ratings):
    rating_weight = 0.6
    num_rating_weight = 0.4
    normalized_ratings = (ratings - 0) / (5 - 0) if 0 <= ratings <= 5 else 0
    normalized_num_ratings = (num_of_ratings - 0) / (1000 - 0) if 0 <= num_of_ratings <= 1000 else 0

    credibility_score = (rating_weight * normalized_ratings + num_rating_weight * normalized_num_ratings) * 100
    credibility_score = max(1, min(credibility_score, 100))
    return credibility_score

def isCredible(ratings_input, num_of_ratings_input):
    THRESHOLD = 30
    if (calculate_credibility_score(ratings_input, num_of_ratings_input) >= THRESHOLD):
        return 1
    else:
        return 0   
    
def isDarkPattern(ratings, no_of_ratings, actual_price, discount_price):
    if actual_price is not None and discount_price is not None:
        diff_percent = ((actual_price - discount_price) / actual_price) * 100
        
        features = np.array([[diff_percent,actual_price]])
        hasMisleadingPrice = model.predict(features)[0]

        is_credible = isCredible(ratings, no_of_ratings)
        isNotCredible = 1 - is_credible
        if diff_percent > 80 and diff_percent <= 100:
            prices_wt = 0.8
        elif 50 < diff_percent <= 80:
            prices_wt = 0.6
        elif 30 < diff_percent <= 50:
            prices_wt = 0.5
        else:
            prices_wt = 0.1
        ratings_wt = 1.0 - prices_wt

        score = (ratings_wt * isNotCredible) + (prices_wt * hasMisleadingPrice)
        THRESHOLD = 0.5

        if score >= THRESHOLD:
            print("The product has potentially MISLEADING information...")
            return 0
        else:
            print("The product has arbitrarily CORRECT information...")
            return 1
    else:
        print("Error: 'None' data is encountered...")
        return None 

def scrape_amazon_product_info(product_link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    response = requests.get(product_link, headers=headers)
    
    if response.status_code == 200:
        print("status_code : 200 -> connection established with Amazon servers...")
        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            product_name_tag = soup.find("span", attrs={"id": 'productTitle'})
            productName = product_name_tag.text.strip()
        except AttributeError:
            productName = "N/A"

        try:
            discount_price_tag = soup.find('span', {'class': 'a-offscreen'})
            discount_price_str = discount_price_tag.text.strip()
            discountPrice = float(discount_price_str.replace('₹', '').replace(',', '').strip()) if discount_price_str else None
        except (AttributeError, ValueError):
            actualPrice = None

        try:
            discount_percent_tag = soup.find('span', {'class': 'savingsPercentage'})
            discountPercent = discount_percent_tag.text.strip()
        except AttributeError:
            discountPercent = "N/A"

        try:
            actual_price_tag = soup.find("span", {'class': 'a-price a-text-price'})
            actualPrice = str(actual_price_tag.text.replace('₹', '').replace(',', '').strip())
            l = len(actualPrice)
            actualPrice = float(actualPrice[:l//2])
        except AttributeError:
            actualPrice = None

        try:
            ratings_tag = soup.find("span", attrs={'class': 'a-icon-alt'})
            ratings = float(ratings_tag.text.split()[0])
        except AttributeError:
            ratings = None

        try:
            no_of_ratings_tag = soup.find("span", attrs={'id': 'acrCustomerReviewText'})
            noOfRatings = int(no_of_ratings_tag.text.split()[0].replace(',', ''))
        except AttributeError:
            noOfRatings = None

        product_info = {
            'product_name': productName,
            'actual_price': actualPrice,
            'discount_percent': discountPercent,
            'discount_price': discountPrice,
            'ratings': ratings,
            'no_of_ratings': noOfRatings
        }

        print("Scraping the site...")
        for key, value in product_info.items():
            print("{}: {}".format(key, value))
        return product_info

    else:
        print(f"status_code : {response.status_code} -> connection not established with Amazon servers...")


def addtoDB(product_name, ratings, no_of_ratings, actual_price, discount_price):
    try:
        df = pd.read_excel('user_data.xlsx')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['product_name', 'main_category', 'ratings', 'no_of_ratings', 'actual_price', 'discount_price'])

    new_data = {'product_name': product_name,
                'ratings': ratings,
                'no_of_ratings': no_of_ratings,
                'actual_price': actual_price,
                'discount_price': discount_price}

    df = df._append(new_data, ignore_index=True)
    df.to_excel('user_data.xlsx', index=False)
    print("DataBase updated with recent product information.....")

def analyze_product(product_name,ratings,no_of_ratings,actual_price,discount_price):
    result = isDarkPattern(ratings,no_of_ratings,actual_price, discount_price)
    st.subheader("**Analysis Results**:")
    st.write(f"**Product Name**:\t {product_name}")
    st.write(f"**Ratings**:\t {ratings}")
    st.write(f"**Number of Ratings**:\t {no_of_ratings}")
    st.write(f"**Actual Price**:\t {actual_price}")
    st.write(f"**Discounted Price**:\t {discount_price}")
    if result == 1:
        st.subheader("The product has arbitrarily CORRECT information")
        st.image("img/tick.jpg",width=350)
    else:
        st.subheader("The product has potentially MISLEADING information")
        st.image("img/cross.png",width=350)

    
def main():
    st.set_page_config(
        page_title="Product Integrity in E-Commerce",
        page_icon=":globe_with_meridians:",
        layout="wide",
    )

    st.title("PRODUCT INTEGRITY IN E-COMMERCE")

    col1, col2 = st.columns(2)

    with col1:
        st.image("img/dpbh.png", width=550)
        st.write("A solution to Dark Patterns in E-Commerce")
        st.subheader("CHECK FOR MISLEADING PRODUCT INFO", divider='rainbow')
        st.text("This tool is compatible with Amazon E-Commerce Site")
        col3, col4, col5 = st.columns(3)
        with col4:
            st.image("img/amazon.png", width=150)
        st.write("This tool targets the identification and mitigation of two prevalent dark patterns :")
        st.write("->   **Misleading Product Information:**   Deceptive pricing strategies, specifically the false inflation of prices followed by presenting a seemingly substantial discount, mislead consumers. Our focus lies in recognizing this pattern of misleading crucial information.")
        st.write("->   **Dark Pattern in User Ratings:**   The misuse of rating systems leads to misconceptions, where a high number of 5-star ratings might not truly reflect a product's quality compared to a larger set of moderately rated reviews.")

        st.markdown('<p style="text-align:center;">--- powered by INCEPTION ---</p>',unsafe_allow_html=True)

    with col2:
        st.subheader("Amazon URL",divider='green')
        st.text("Paste the amazon link or URL here...")
        form1 = st.form("productLink")
        link = form1.text_input("Amazon Link / URL", key='link')
        analyze_button = form1.form_submit_button("Analyze")
        if analyze_button:
            prodInfo_dict = scrape_amazon_product_info(link)
            analyze_product(prodInfo_dict['product_name'],prodInfo_dict['ratings'],prodInfo_dict['no_of_ratings'],prodInfo_dict['actual_price'],prodInfo_dict['discount_price'])
            addtoDB(prodInfo_dict['product_name'],prodInfo_dict['ratings'],prodInfo_dict['no_of_ratings'],prodInfo_dict['actual_price'],prodInfo_dict['discount_price'])
        st.subheader("--------------------------------------------------------------------")
        st.subheader("Product Details",divider='green')
        st.text("Product Name is optional, but other fields are mandatory.")
        form = st.form("productInfoForm")

        product_name = form.text_input("Product Name (optional)", key="product_name")
        ratings = form.number_input("Ratings", min_value=0.0,max_value=5.0, step=0.10, key="ratings")
        no_of_ratings = form.number_input("Number of Ratings", min_value=0, key="no_of_ratings")
        actual_price = form.number_input("Actual Price", min_value=0,step=10, key="actual_price")
        discount_price = form.number_input("Discounted Price", min_value=0,step=10, key="discount_price")

        analyze_button = form.form_submit_button("Analyze")

        if analyze_button:
            analyze_product(product_name,ratings,no_of_ratings,actual_price,discount_price)
            addtoDB(product_name,ratings,no_of_ratings,actual_price,discount_price)

if __name__ == "__main__":
    main()