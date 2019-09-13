import React from 'react';
import Loader from 'react-loader-spinner';

const URL = 'http://34.222.190.54/api/search/disease_search?query='


const ListItem = ({value}) => (
  <li>{value}</li>
);

const List = ({items}) => (
	<div>
  <ul>
    {
      items.map((item, i) => <ListItem key={i} value={item}/>)
    }
  </ul>
	</div>
);


const NamedList = ({items, title, loading}) => (<div>
<p className={items.length === 0 || loading? 'hidden':''}>{title}</p>
                        <List items={items} className={loading? 'hidden': ''}/>
</div>)


export class SearchBox extends React.Component{
	constructor(props) {
		super(props);
		// create a ref to store the text input from the input box
		this.input = React.createRef();
		this.name = React.createRef();
		this.definition = React.createRef();
		this.ancestry = [];
		this.sibls = [];
		this.search = this.search.bind(this);
		this.synonyms = [];
		this.child_nodes = [];
		this.state = {loading: false, search_results: null};
	}

	search(){
		this.setState({loading: true});
		let currentInput = this.input.current.value;
		fetch(URL + currentInput)
			.then(function(response){
				return response.json();
			}).then((json) => {
				if(json['result']){
					console.log(JSON.stringify(json));
					let result = json['result'];
					this.name.current.innerText = result['name'];
					this.definition.current.innerText = result['definition'];
					this.ancestry = result['tree'].split('.');
					this.sibls = result['sibls'];
					this.synonyms = result['synonym'];
					if(this.synonyms == "Key Not found"){
						console.log(this.synonyms);
						this.synonyms = [];
					}
					if(result['childs']){
						console.log(result['childs']);
						this.child_nodes = result['childs'];
					}
					else{
						this.child_nodes = [];
					}
					this.setState({loading:false,
						search_results: json});
				}
				else{
					this.name.current.innerText = "Could not find " + '"' + currentInput + '"' + ' in our database';
					this.definition.current.innerText = '';
                                        this.ancestry = [];
                                        this.sibls = [];
                                        this.synonyms = [];
					this.setState({loading:false});
				}

			});
	}

	render(){
		return (
			<div>
			<h1>ICD11 Search</h1>
			<div>
			<input ref={this.input}></input>
			<button onClick={this.search}>Search</button>
			</div>
			<div id="results_container">
			<Loader
         type="TailSpin"
         color="#00BFFF"
         height="100"
         width="100"
          className={this.state.loading ? '': 'hidden'}
      />
			<div id='results'>
			<p ref={this.name} 
			className={this.state.loading? 'hidden': ''}></p>
			<p ref={this.definition}
                        className={this.state.loading? 'hidden': ''}></p>
			<NamedList items={this.ancestry} title={'Ancestry'} loading={this.state.loading}/>
			<NamedList items={this.sibls} title={"Sibling nodes"} loading={this.state.loading}/>
			<NamedList items={this.synonyms} title={"Synonyms"} loading={this.state.loading}/>
			<NamedList items={this.child_nodes} title={"Child nodes"} loading={this.state.loading}/>
			</div>

			</div>
			</div>
		)
	}
}

