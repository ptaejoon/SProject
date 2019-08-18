import React from "react";
import styled from "styled-components";
import { SearchBar } from 'react-native-elements';
import styles from "../../styles";
import { Text } from "react-native";
import axios from "axios";
import SearchResult from "./SearchResult"
import SearchResultList from "./SearchResultList"
import Category from "./Category"


const View = styled.View`
  justify-content: center;
  align-items: center;
  flex: 1;
`;

export default class App extends React.Component {


//초기 state 설정
  state = {
    search: '',
    data: [],
    showList: false,
    showResultPage: false,
    title: [],
    productName: '',
  };

  //검색결과를 가지고 오는 함수
  getResult = async search => {
    await axios.get("http://localhost:8000/BeginVegan/pdList/?name="+this.state.search)  
    .then(resp=>{
      this.setState({data : resp.data.results});
      this.setState({showList: true})
      console.log(this.state.showList)
    })  
    .catch(error=>{
      console.log("error")
      this.setState({showList: false})
    });

    // if(typeof this.state.data !== 'undefined' && this.state.data.length > 0){
    // }
  }

//2글자 이상 검색부터 자동완성 실행
  autocomplete = async search =>{
    await this.setState({search: search})
    if(search.length>=2){
      await this.getResult(search)
    }
    else{
      await this.setState({showList: false})
      console.log(search.length)
    }
    this.setState({showResult: false})
    console.log(this.state.showList)
  }
  
  goResult = name =>{
    this.setState({showResult: true})
    this.setState({productName: name})
    this.setState({search: name})
  }
  
  render() {
    const { search } = this.state;

    return (
      <>
      <SearchBar
        inputContainerStyle={{ backgroundColor: 'white' }}
        containerStyle={{ backgroundColor: styles.green, borderTopWidth: 0, borderBottomWidth: 0,}}
        placeholder="나에게 맞는 제품은 뭐가 있을까?"
        onChangeText={this.autocomplete}  //자동완성
        value={search}
        onSubmitEditing= {()=>{
          return ;
        }}
      />
      {
        this.state.showResult ?
        <SearchResult name={this.state.productName}/> :

        this.state.showList ? 
        <SearchResultList 
          name={this.state.data.map(
          temp=>{ return {key: temp.title}})}

          goResult={this.goResult}

          /> 
          
          : 
          <Category />
  
        }
      
      </>





    );
        
  }
}