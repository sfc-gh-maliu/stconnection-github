from streamlit.connections import ExperimentalBaseConnection
import requests
import streamlit as st
import pandas as pd

class GithubConnection(ExperimentalBaseConnection):

    def _connect(self, **kwargs) -> requests.Session:
        session = requests.Session()
        session.headers['Authorization'] = 'Bearer ' + st.secrets['connections']['github']['token']
        return session

    def search_code(self, keyword, **kwarg):
        page = 1
        per_page = 100 
        params = {
            'page':page,
            'per_page':per_page
        }

        search_url = f"https://api.github.com/search/code?q={keyword}+language:python"

        response = self._instance.get(search_url, params = params)
        if response.status_code == 200:
            response_data = response.json()
            
            df = pd.DataFrame(response_data)
            df['url'] = df['items'].apply(lambda x:x['html_url']) #return url 
            df['repository'] = df['items'].apply(lambda x:x['repository']['full_name']) #return repo
            df.drop(columns=['items'], inplace=True)

            return df
        else:
            return None

    def get_github_issues(self):
        # API endpoint for searching issues

        owner = "streamlit"
        repo_name = "streamlit"

        search_url = f"https://api.github.com/repos/{owner}/{repo_name}/issues"

        # Make the API call using the 'requests' library
        response = self._instance.get(search_url)
        return response.json()[0]

        # # Check if the API call was successful (status code 200)
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            # Handle error scenarios here
            return None