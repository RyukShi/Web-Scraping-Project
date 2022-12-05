from re import search, escape, IGNORECASE
from time import time


technologies = [
    # Python Frameworks
    'Django', 'Flask', 'TurboGears', 'Falcon', 'CherryPy', 'Pyramid', 'Grok', 'Web2Py', 'Bottle', 'Tornado', 'BlueBream', 'Hug',
    # PHP Frameworks
    'Symfony', 'Laravel', 'CodeIgniter', 'CakePHP', 'Yii', 'Laminas', 'Phalcon', 'Fat-Free', 'Lumen', 'Slim', 'Flight', 'PHPixie',
    # JavaSript Frameworks
    'Vue.js', 'Ext JS', 'Angular', 'React', 'Ember.js', 'Svelte', 'Meteor', 'Mithril.js', 'Backbone.js', 'Polymer.js', 'Node.js', 'Aurelia',
    # Main tech
    'C', 'C++', 'C#', 'F#', 'Java', 'Python', 'Ruby', 'Rust', 'TypeScript', 'PHP', 'Sass',
    # Java Frameworks
    'Apache Struts', 'Spark', 'Hibernate', 'JavaServer Faces', 'Spring', 'Dropwizard', 'Vaadin', 'Grails', 'Apache Hadoop',
    # Gestion de projet
    'Jira', 'Atlassian', 'Git', 'GitHub', 'GitLab', 'Trello',
    # Services d'hébergement
    'Firebase', 'Supabase',
    # SGBD
    'PostgreSQL', 'MySQL', 'MariaDB', 'SQLite', 'MongoDB', 'Altibase', 'Microsoft SQL Server', 'Oracle', 'Redis', 'Elasticsearch', 'Cassandra',
    # Unit Tests & UI Tests
    'PHPUnit', 'Selenium', 'Puppeteer', 'Junit', 'NUnit', 'JMockit', 'EMMA', 'Jest', 'AVA', 'Mocha', 'Jasmine', 'Cypress',
    # Others
    '.NET', 'RabbitMQ', 'NgRx',
    # JS libraries
    'RxJS', 'Redux'
]

start_time = time()

d = "Are you an experienced Fullstack Software Engineer looking for your next challenge? The Sportsbook Area with Product Development is now hiring! We have a world-class Sportsbook, developed in-house by our dedicated Sportsbook tech team. Our Sportsbook Platform is ours – from our Architecture to our Trading teams – we have an in-house platform which hosts our brands offering Sportsbetting for our customers. From the tools our traders use to the cutting edge features our customers use to bet on various sports – our teams are the backbone to making this happen!The WowOur product is really used by hundred and thousands of users, so your work is definitely visible! We are operating in a very competitive market therefore we MUST use latest technologies.Take a look at some of our brands what we are working on Betsafe, NordicBetOur aim is to create the best performance, functionality and user experience in the iGaming industry! As part of our Sportsbook tech team – a high performance, throughout and availability product serving many brands (20+), you will be key in ensuring that the team delivers the required business value.You will join more than 100 agile people distributed across 3 locations in 2 countries, working with a wide variety of technologies from Angular and Typescript to .NET Core, C#LI- and RabbitMQ. We are working in cross functional teams consisting of architects, developers, QAs, database experts and devops staff.Would you like to know more about the background of sports betting? Check the interview with our colleague here.At Betsson Group we work with a Hybrid Work From Home (WFH) model, giving you the flexibility of working 2 days in the office and 3 days at home.What's in it for you?This is your chance to be working on a world-leading, high performance, high availability and high throughput multi-brand betting platform.Our main product is a sports betting web application; a large, single page application built using Angular and ngRx as its main front-end technologies. Working on this product is a great opportunity to experience front-end development on a large scale with up-to-date technologies and a strong end-user focus.To give you an idea of the data behind our applications, here are some numbers10,000 different leagues1100 matches and 500-600.000 bets on a single SaturdayYou will be working with the following technologiesAngular 9TypeScript 3Redux pattern for state management through ngRxRxJSAngular MaterialSassHTML5You are good atJavaScriptany JavaScript based UI frameworkHTML, CSSInteracting with REST APIsCommunicating in EnglishExtra awesomeExperience in using Angular2+, Redux and RxJS.Net/C#LI- knowledge in ASP.NET MVC, Web API and WCFExperience in using responsive designSQL server, writing queries and tuning performanceImplementing distributed and multi-tier/micro-service systemsA flavour of what you'll be doingYou will be part of an end-to-end agile team with a strong feature focus, consisting of developers, test specialists, automation engineers and UX specialists. Team members are expected to be involved in all aspects of software development from making sure that the architecture and design is as good as we can make it, to writing code, unit and end-to-end tests and manage our data models.You will work both on designing and implementing new features as well as analyzing the system and improve architecture and technical excellence.What We OfferMuch like riding a rollercoaster, sometimes life at Betsson can be lightning fast with twists and turns but always FUN! Then again, what else would you expect from a business 75% millennial and 1700 strong, spread across 7 offices with 900 based out of our Malta HQ alone! We recognise it may not be for the faint-hearted, but if you’re a go-getter, initiator and adrenaline junkie, always striving to push the boundaries and challenge yourself, then you’ll fit right in.At Betsson Group we work with a Hybrid Work From Home (WFH) model, giving you the flexibility of working 2 days in the office and 3 days at home.We offer numerous challenges where your skills will be put to good use! We encourage innovation, independence and celebrate success where you will be part of multi-cultural and diverse company, with people from all over the world.Challenge accepted?By submitting your application, you understand that your personal data will be processed as set out in our Privacy Policy.átai"

re_process = [tech for tech in technologies if search(
    fr"(?!\B\w){escape(tech)}(?<!\w\B)", d, IGNORECASE)]

print(re_process)

print(f"execution time : {(time() - start_time) * 10**3} ms")
