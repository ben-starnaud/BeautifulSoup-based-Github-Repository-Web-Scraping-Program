from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import requests
import re
import json

# Gets User/Org Information
def get_user_data(username):
    url = f"https://github.com/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        user_page = BeautifulSoup(response.content, "html.parser")
        is_org = False
        
        # ID
        meta_tags = user_page.find_all('meta')
        pr_amount = None
        for meta_tag in meta_tags:
            name_value = meta_tag.get("name")
            if name_value != None :
                if "user_id" in name_value:
                    content_value = meta_tag.get("content")
                if "hovercard" in name_value:
                    org_id = meta_tag.get("content")
                    parts = org_id.split(":")
                    content_value = int(parts[1])
                    is_org = True
                if "description" in name_value:
                    repo_sentance = meta_tag.get('content')
                    sentance_nums = re.findall(r'\d+', repo_sentance)
                    if len(sentance_nums) >= 1:
                        pr_amount = sentance_nums[0]
        
        # User
        if is_org:
            is_user = "Organization"
        else:
            is_user = "User"

        # If the account is a USER
        if is_org is False :

            # Avatar 
            avatar_img = user_page.find('img', {'alt':'Avatar'})
            avatar_url = avatar_img.get('src') if avatar_img else None

            # Name 
            name_element = user_page.find('span', class_='p-name vcard-fullname d-block overflow-hidden')
            if name_element and name_element.text.strip():
                user_name = name_element.text.strip()
            else:
                user_name = None

            # Login
            login_element = user_page.find('span', class_='p-nickname vcard-username d-block')
            if login_element and login_element.text.strip():
                login_name = login_element.text.strip()
            else:
                login_name = None
            
            # Company Name
            company_name = user_page.find('span',class_='p-org')
            if company_name and company_name.text.strip():
                comp_name = company_name.text.strip()
            else:
                comp_name = None

            # Location
            loc = user_page.find('span',class_='p-label')
            if loc and loc.text.strip():
                loc_name = loc.text.strip()
            else:
                loc_name = None

            # Public Repos
            num_public_repo = user_page.find('span', class_='Counter')
            if num_public_repo and num_public_repo.text.strip():
                pr_amount = num_public_repo.text.strip()
            else:
                pr_amount = "0"
            
            # Followers
            followers_element = user_page.find('a', href=f"https://github.com/{login_name}?tab=followers")
            if followers_element:
                followers_text = followers_element.find('span', class_='text-bold color-fg-default')
                if followers_text:
                    followers = followers_text.text.strip()
                else:
                    followers = "0"
            else:
                followers = "0"
            
            
            # Following
            following_element = user_page.find('a', href=f"https://github.com/{login_name}?tab=following")
            if following_element:
                following_text = following_element.find('span', class_='text-bold color-fg-default')
                if following_text:
                    following = following_text.text.strip()
                else:
                    following = "0"
            else:
                following = "0"

            # Acccounts (Twitter and Blog)  
            platform_headers = user_page.find_all('a', rel='nofollow me', class_='Link--primary')
            href_list = []
            for name in platform_headers:
                href = name['href']  # Get the 'href' attribute value from the <a> tag
                href_list.append(href)   
            twitter_username = None
            for link in href_list:
                if "twitter" in link:
                    twitter_username = link.split('/')[-1]

            # Blog
            blog_element = user_page.find("ul", class_="vcard-details")
            if blog_element.find('li', itemprop="url"):
                blog_closer = blog_element.find("li", itemprop = "url")
                blog_closer1 = blog_closer.find("a", rel = "nofollow me", class_= "Link--primary")
                blog = blog_closer1.text.strip()
            else:
                blog = ""
            
            # Bio 
            bio_top = user_page.find('div', class_='p-note user-profile-bio mb-3 js-user-profile-bio f4')
            if bio_top :
                bio = bio_top.get('data-bio-text')
                bio_text = bio
                if bio_text == "":
                    bio_text = None
            else:
                bio_text = None

        # If the account is an ORGANISTION
        else:
            
            # Avatar 
            avatar_img = user_page.find('img')
            full_url = avatar_img.get('src') if avatar_img else None
            parsed_url = urlparse(full_url)
            query_params = parse_qs(parsed_url.query)
            if 's' in query_params:
                query_params.pop('s')
            modified_query = urlencode(query_params, doseq=True)
            avatar_url = urlunparse(parsed_url._replace(query=modified_query))

            # Login
            login_element = user_page.find_all('meta')
            if login_element != None:
                for meta in login_element:
                    meta_prop = meta.get('property')
                    if meta_prop != None:
                        if "profile:username" in meta_prop:
                            login_name = meta.get('content')
                   
        
            # Name 
            name_element = user_page.find('h1', class_='h2 lh-condensed')
            if name_element and name_element.text.strip():
                user_name = name_element.text.strip()
            else:
                user_name = None
            
            # Company Name
            comp_name = None

            # Location
            loc = user_page.find('span',itemprop='location')
            if loc and loc.text.strip():
                loc_name = loc.text.strip()
            else:
                loc_name = None

            # Followers
            followers_text = user_page.find('span', class_='text-bold color-fg-default')
            if followers_text:
                followers = followers_text.text.strip()
            else:
                followers = "0"
            
            
            # Following
            following_element = user_page.find('a', href=f"https://github.com/{login_name}?tab=following")
            if following_element:
                following_text = following_element.find('span', class_='text-bold color-fg-default')
                if following_text:
                    following = following_text.text.strip()
                else:
                    following = "0"
            else:
                following = "0"

            # Twitter Acccounts  
            twitter_username = None
            top_sect = user_page.find('div', class_="container-xl pt-4 pt-lg-0 p-responsive clearfix")
            if top_sect != None:
                accounts = top_sect.find('div',class_="d-md-flex flex-items-center mt-2")
                li = accounts.find_all('li')
                for acc in li:
                    a_value = acc.find('a')
                    if a_value != None:
                        link = a_value.get('href')
                        if "followers" not in link:
                            if "https://twitter.com" in link:
                                twitter_username = link.split('/')[-1]

            # Blog
            blog_element = None 
            if user_page.find('ul',class_="d-md-flex list-style-none f6 has-location has-blog"):
                blog_element = user_page.find('ul',class_="d-md-flex list-style-none f6 has-location has-blog")
            elif user_page.find('ul',class_="d-md-flex list-style-none f6 has-blog"):
                blog_element = user_page.find('ul',class_="d-md-flex list-style-none f6 has-blog")
            elif user_page.find('ul',class_="d-md-flex list-style-none f6 has-location has-blog has-email"):
                blog_element = user_page.find('ul',class_="d-md-flex list-style-none f6 has-location has-blog has-email")
            elif user_page.find('ul',class_="d-md-flex list-style-none f6 has-blog has-email"):
                blog_element = user_page.find('ul',class_="d-md-flex list-style-none f6 has-blog has-email")  
            if blog_element != None:
                blog_intro = blog_element.find_all('li', style="max-width: 230px")  
                for elem in blog_intro:
                    if elem.find('a', rel= "nofollow"):
                        blog_almost = elem.find('a',rel="nofollow")
                        if blog_almost != None:
                            blog = blog_almost["href"]
                            if "twitter" not in blog:
                                break
                            break
            else:
                blog = ""
            # Bio
            bio_top = user_page.find('div', class_="container-xl pt-4 pt-lg-0 p-responsive clearfix")
            bio = bio_top.find('div', class_='color-fg-muted')
            if bio != None and bio.text.strip():
                bio_text = bio.text.strip()
            else:
                bio_text = None

        
        user_data = {
            "login": login_name, 
            "id": content_value, 
            "avatar_url": avatar_url, 
            "url": f"https://api.github.com/users/{login_name}", 
            "html_url": f"https://github.com/{login_name}",  
            "type": is_user,
            "name": user_name,
            "company": comp_name,
            "blog": blog, 
            "location": loc_name,
            "bio": bio_text,
            "twitter_username": twitter_username,
            "public_repos": pr_amount,
            "followers": followers,
            "following": following
        }

        return user_data
    return None

def list_user_repos(username):

    url = f"https://github.com/{username}"
    response = requests.get(url)

    if response.status_code == 200:

        intropage = BeautifulSoup(response.content, "html.parser")
        
        # ID
        meta_tags = intropage.find_all('meta')
        for meta_tag in meta_tags:
            name_value = meta_tag.get("name")
            if name_value != None :
                if "user_id" in name_value:
                    is_org = False
                if "hovercard" in name_value:
                    is_org = True

        # Login
        login_element = intropage.find_all('meta')
        if login_element != None:
            for meta in login_element:
                meta_prop = meta.get('property')
                if meta_prop != None:
                    if "profile:username" in meta_prop:
                        login_name = meta.get('content')
                        

        if is_org is False : #                USER
            
            page = 1;
            
            has_page = True
            repositories = []
            
            while has_page == True:

                if page == 1:
                    url = f"https://github.com/{username}?tab=repositories" 
                else:
                    url = f"https://github.com/{username}?page={page}&tab=repositories"


                response = requests.get(url)
                if response.status_code == 200:
                    
                    soup = BeautifulSoup(response.content, "html.parser")
                    repo_classes = [
                        "col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public source",
                        "col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public fork"
                    ]
                    all_repos = soup.find_all('li', class_=repo_classes)
                    
                    for repo in all_repos:
                        
                        # Forked 
                        forked = False
                        if "fork" in repo.get('class'):
                            forked = True
                    
                        # Name
                        name = repo.find('a', itemprop="name codeRepository")
                        full_name = name.text.strip()

                        # Description
                        des = repo.find('p', class_="col-9 d-inline-block color-fg-muted mb-2 pr-4", itemprop="description")
                        if des and des.text.strip():
                            repo_des = des.text.strip()
                        else:
                            repo_des = None

                        # Language
                        repo_lang = repo.find('span', itemprop="programmingLanguage")
                        if repo_lang and repo_lang.text.strip():
                            repo_language = repo_lang.text.strip()
                        else:
                            repo_language = None

                        # Amount of Forks 
                        forks = repo.find('a',class_="Link--muted mr-3", href=f"/{login_name}/{full_name}/forks")
                        if forks and forks.text.strip():
                            num_forks = forks.text.strip()
                        else:
                            num_forks = "0"
                        
                        # Amount of Stargazers 
                        stargazers = repo.find('a',class_="Link--muted mr-3", href=f"/{login_name}/{full_name}/stargazers")
                        if stargazers and stargazers.text.strip():
                            num_stargazers = stargazers.text.strip()
                        else:
                            num_stargazers = "0"

                        # Archived and Private
                        archived = False
                        is_private = False
                        divs = repo.find('div', itemscope="itemscope")
                        if divs is not None:
                            archive = divs.get('class')
                            if "archived" in archive:
                                archived = True
                            if "Private" in archive :
                                is_private = True

                        # Pushed Time
                        p_time = repo.find('div', class_="f6 color-fg-muted mt-2")
                        if p_time != None:
                            time = p_time.find('relative-time')
                            p_time = time.get('datetime')

                        # Extract more info
                        more_data = extract_extras(login_name, full_name) 

                        repo_data = {
                            "name" : full_name,
                            "private": is_private,
                            "html_url": f"https://github.com/{login_name}/{name.text.strip()}",
                            "description": repo_des,
                            "fork": forked,
                            "url": f"https://api.github.com/repos/{login_name}/{name.text.strip()}",
                            "language": repo_language,
                            "forks_count": num_forks,
                            "stargazers_count": num_stargazers,
                            "watchers_count": num_stargazers,
                            "archived": archived,
                            "pushed_time": p_time
                        }

                        
                        formatted_repo_data = json.dumps(repo_data, indent=4)
                        repo_data = json.loads(formatted_repo_data)
                        more_repo_data = json.loads(more_data)
                        combined_data = {**repo_data, **more_repo_data} 
                        repositories.append(combined_data)

                    
                    # Next Page
                    page_container = soup.find('div',class_="paginate-container")
                    if page_container != None:
                        pages = page_container.find('a', class_="next_page")
                        if pages != None:
                            page = page + 1
                        else:
                            sorted_repos = sorted(repositories, key=lambda x: (extract_numeric_part(x["name"]), x["name"]))
                            return sorted_repos
                    else:
                        sorted_repos = sorted(repositories, key=lambda x: (extract_numeric_part(x["name"]), x["name"]))
                        return sorted_repos
                    
            
        else:  #     ORGANISATION
            page = 1;
            
            has_page = True
            repositories = []
            
            while has_page == True:

                if page == 1:
                    url = f"https://github.com/orgs/{username}/repositories" 
                else:
                    url = f"https://github.com/orgs/{username}/repositories?page={page}"
            
                response = requests.get(url)
                if response.status_code == 200:
                    
                    soup = BeautifulSoup(response.content, "html.parser")
                    all_repos = soup.find_all('li', class_="Box-row")
                    
                    for repo in all_repos:
                    
                        # Forked 
                        fork = repo.find('span', class_="color-fg-muted mb-1 f6")
                        if fork != None:
                            forked = True
                        else:
                            forked = False
                    
                        # Name 
                        name = repo.find('a', itemprop="name codeRepository")
                        full_name = name.text.strip()


                        # Private, Public 
                        is_repo_private = repo.find('span', class_="Label Label--secondary v-align-middle ml-1 mb-1")
                        if "Public" or "Public template" in is_repo_private.text.strip():
                            is_private = False
                        else:
                            is_private = True

                        # Archived
                        archived = False
                        divs = repo.find('div', itemscope="itemscope")
                        if divs is not None:
                            archive = divs.get('class')
                            if "archived" in archive:
                                archived = True

                        # Description
                        des = repo.find('p', class_="color-fg-muted mb-0 wb-break-word", itemprop="description")
                        if des and des.text.strip():
                            repo_des = des.text.strip()
                        else:
                            repo_des = None

                        # Language
                        repo_lang = repo.find('span', itemprop="programmingLanguage")
                        if repo_lang and repo_lang.text.strip():
                            repo_language = repo_lang.text.strip()
                        else:
                            repo_language = None

                        # Amount of Forks 
                        forks = repo.find('a',class_="Link Link--muted mr-3", href=f"/{login_name}/{full_name}/forks")
                        if forks and forks.text.strip():
                            num_forks = forks.text.strip()
                        else:
                            num_forks = "0"
                        
                        # Amount of Stargazers 
                        stargazers = repo.find('a',class_="no-wrap Link Link--muted mr-3", href=f"/{login_name}/{full_name}/stargazers")
                        if stargazers and stargazers.text.strip():
                            num_stargazers = stargazers.text.strip()
                        else:
                            num_stargazers = "0"

                        # Pushed Time
                        p_time = repo.find('div', class_="color-fg-muted f6 mt-2")
                        if p_time != None:
                            time = p_time.find('relative-time')
                            p_time = time.get('datetime')

                            
                        # Extract more info
                        more_data = extract_extras(login_name, full_name) 


                        repo_data = {
                            "name" : full_name,
                            "private": is_private,
                            "html_url": f"https://github.com/{login_name}/{name.text.strip()}",
                            "description": repo_des,
                            "fork": forked,
                            "url": f"https://api.github.com/repos/{login_name}/{name.text.strip()}",
                            "language": repo_language,
                            "forks_count": num_forks,
                            "stargazers_count": num_stargazers,
                            "watchers_count": num_stargazers,
                            "archived": archived,
                            "pushed_time": p_time
                        }

                        
                        formatted_repo_data = json.dumps(repo_data, indent=4) 
                        repo_data = json.loads(formatted_repo_data)
                        more_repo_data = json.loads(more_data)
                        combined_data = {**repo_data, **more_repo_data}
                        repositories.append(combined_data)

                    # Next Page
                    page_container = soup.find('div', role="navigation", class_="pagination")
                    if page_container != None:
                        pages = page_container.find('a', class_="next_page")
                        if pages != None:
                            page = page + 1
                        else:
                            sorted_repos = sorted(repositories, key=lambda x: (extract_numeric_part(x["name"]), x["name"]))
                            return sorted_repos
                    else:
                        sorted_repos = sorted(repositories, key=lambda x: (extract_numeric_part(x["name"]), x["name"]))
                        return sorted_repos
   


def extract_extras(username, full_name):
    url = f"https://github.com/{username}/{full_name}"
    response = requests.get(url)
   
    
    if response.status_code == 200:
        more_info = BeautifulSoup(response.content, "html.parser")

        # Repo ID
        repo_tags = more_info.find_all('meta')
        for meta_tag in repo_tags:
            name_value = meta_tag.get("name")
            if name_value != None :
                if "user_id" in name_value:
                    repo_user_id = meta_tag.get("content")
                if "repository_id" in name_value:
                    repo_id = meta_tag.get("content")
                          
        # Default Branch
        branches = more_info.find('summary', class_= "btn css-truncate")
        if branches != None:
            branch = branches.find('span', class_="css-truncate-target")
            default_branch = branch.text.strip()
        else:
            default_branch = "main"

        # Topics
        all_topics = []
        topics = more_info.find('div', class_="f6")
        if topics != None:
            sub_topics = topics.find_all('a', class_="topic-tag topic-tag-link")
            for each_topic in sub_topics:
                all_topics.append(each_topic.text.strip())  
        all_topics = sorted(all_topics)       
        
        
        if len(all_topics) != 0:
            topics_str = all_topics
        else:
            topics_str = '[]'
    
        # Homepage
        if more_info.find("span", class_ = "flex-auto min-width-0 css-truncate css-truncate-target width-fit"):
            home_element = more_info.find("span", class_ = "flex-auto min-width-0 css-truncate css-truncate-target width-fit")
            if home_element.find("a"):
                homepage = home_element.find("a")
                homepage = homepage["href"]
            else:
                homepage = ""
        else: 
            homepage = None

        #Discussions, Projects, Issues and Pull Requests
        has_discuss = False
        has_proj = False
        has_issues_bar = False
        has_pr_bar = False
        disc = more_info.find('ul',class_="UnderlineNav-body list-style-none")
        if disc != None:
            all_li = disc.find_all('li')
            for li in all_li:
                has_a = li.find('a')
                if has_a != None:
                    id_ = has_a.get('id')
                    if "projects-tab" in id_:
                        has_proj = True
                    if "discussions-tab" in id_:
                        has_discuss = True
                    if "pull-requests-tab" in id_:
                        pr = get_prs(username,full_name)
                        has_pr_bar = True
                    if "issues-tab" in id_:
                        just_open_issues = get_open_issues(username,full_name)
                        has_issues_bar = True
                        
    
        # Open Issues
        if has_issues_bar and has_pr_bar:
            all_open_issues = just_open_issues + pr
        elif has_issues_bar and has_pr_bar == False:
            all_open_issues = just_open_issues
        elif has_pr_bar and has_issues_bar == False:
            all_open_issues = pr

        
        more_repo_data = {
            "id":repo_id,
            "name": full_name,
            "full_name":f"{username}/{full_name}",
            "owner":{
                "login":username,
                "id":repo_user_id
            },
            "Homepage": homepage,
            "default_branch": default_branch,
            "open_issues_count": all_open_issues, 
            "topics": topics_str, 
            "has_issues": has_issues_bar,
            "has_projects": has_proj,
            "has_discussions": has_discuss
        }

        formatted_more_repo_data = json.dumps(more_repo_data, indent=4)
    return formatted_more_repo_data

                

def get_prs(username, full_name):
    

    url = f"https://github.com/{username}/{full_name}/pulls"
    
    response = requests.get(url)

    if response.status_code == 200:
                    
        pull = BeautifulSoup(response.content, "html.parser")

        amount_text = pull.find('div', class_="d-block d-lg-none no-wrap")
        if amount_text != None:
            texts = amount_text.find('a')
            if texts != None:
                pull_req_text = texts.text.strip()
        
        pull_req_text = pull_req_text.replace("Open", "").strip()
        if "," in pull_req_text:
            pull_req_text = pull_req_text.replace(",", "").strip()

        
        pull_req = int(pull_req_text)

    return pull_req



def get_open_issues(username, full_name):
    
    open_issues = 0

    url = f"https://github.com/{username}/{full_name}/issues"
    
    response = requests.get(url)

    if response.status_code == 200:
                    
        open = BeautifulSoup(response.content, "html.parser")

        amount_text = open.find('div', class_="d-block d-lg-none no-wrap")
        if amount_text != None:
            texts = amount_text.find('a')
            if texts != None:
                open_issues_text = texts.text.strip()
        
        open_issues_text = open_issues_text.replace("Open", "").strip()
        if "," in open_issues_text:
            open_issues_text = open_issues_text.replace(",", "").strip()

        
        open_issues = int(open_issues_text)
            
    return open_issues

def extract_numeric_part(name):
    match = re.search(r'\d+', name)
    return int(match.group()) if match else 0