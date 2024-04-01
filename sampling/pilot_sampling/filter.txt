def convert_country(df):
    df.loc[df['country'] == 'Pologne', 'country'] = 'Poland'
    df.loc[df['country'] == 'Grèce', 'country'] = 'Greece'
    df.loc[df['country'] == 'Russie', 'country'] = 'Russia'
    df.loc[df['country'] == 'Finlande', 'country'] = 'Finland'
    df.loc[df['country'] == 'Slovénie', 'country'] = 'Slovenia'
    df.loc[df['country'] == 'Danemark', 'country'] = 'Denmark'
    df.loc[df['country'] == 'Serbie', 'country'] = 'Serbia'
    df.loc[df['country'] == 'Irlande', 'country'] = 'Ireland'
    df.loc[df['country'] == 'Singapour', 'country'] = 'Singapore'
    df.loc[df['country'] == 'Bahreïn', 'country'] = 'Bahrain'
    df.loc[df['country'] == 'Brésil', 'country'] = 'Brazil'
    df.loc[df['country'] == 'Norvège', 'country'] = 'Norway'
    df.loc[df['country'] == 'Corée du Sud', 'country'] = 'South_Korea'
    df.loc[df['country'] == 'République tchèque', 'country'] = 'Czech_Republic'
    df.loc[df['country'] == 'Nouvelle Zélande', 'country'] = 'New_Zealand'
    df.loc[df['country'] == 'Irlande', 'country'] = 'Ireland'
    df.loc[df['country'] == 'Irlande', 'country'] = 'Ireland'
    
    return df




df = pd.read_csv("users.csv")
df = df.drop(columns=['identifierHash', 'seniorityAsMonths', 'seniorityAsYears', 'countryCode' ])
df = convert_country(df)
df = df.sample(frac=1)
df = df[df['country'].isin([ 'France', 'United_States', 'United_Kingdom', 'Italy', 'Australia', 'Germany', ])]
#'Denmark', 'Finland', 'Netherlands', 'Sweden', 'Spain'
active = df[helper_has_any_field_greater_than(df, ['socialProductsLiked', 'productsListed', 'productsSold',
       'productsPassRate', 'productsWished', 'productsBought'], 0)]
inactive = df[helper_has_fields_compared_to(df, ['socialProductsLiked', 'productsListed', 'productsSold',
       'productsPassRate', 'productsWished', 'productsBought'], 0, 'all', '==')]
inactive = df[df['socialNbFollowers'] > 50]
