import React from "react";
import styled from "styled-components";
import { SearchBar } from 'react-native-elements';
import styles from "../../styles";
import { Text } from "react-native";
import axios from "axios";




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
  };

  getResult = async search => {
    await this.setState({search: search})
    console.log(this.state.search)
    
    if(search.length>=2){
    const data = 
    await axios.get("http://localhost:8000/BeginVegan/pdList/?name="+this.state.search)  
    .then(resp=>{
      console.log(resp.data);
    })  
    .catch(error=>{
      console.log("error")
    });
    await this.setState({data : data});

    console.log(data)
  }
  else{
    console.log(search.length)
  }
  }


// 단어를 칠 때 마다 state 변경 해주고 함수도 실행가능

  autocomplete = name =>{

  }
  
  render() {
    const { search } = this.state;

    return (
      <>
      <SearchBar
        inputContainerStyle={{ backgroundColor: 'white' }}
        containerStyle={{ backgroundColor: styles.green, borderTopWidth: 0, borderBottomWidth: 0,}}
        placeholder="나에게 맞는 제품은 뭐가 있을까?"
        onChangeText={this.getResult}
        value={search}
        onSubmitEditing= {()=>{
          return ;
        }}
      />

        <Text>
          haha
        </Text>

      </>
    );
  }
}