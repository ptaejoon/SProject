import React, { Component } from 'react';
import { FlatList, StyleSheet, Text, View } from 'react-native';
import { TouchableOpacity } from 'react-native-gesture-handler';
import SearchResult from "./SearchResult"


export default class FlatListBasics extends Component {
  constructor(props){
    super(props)
  }

  render() {
    return (
      <View style={styles.container}>
        <FlatList
          data={this.props.name}

          renderItem={({item}) => 
          <TouchableOpacity onPress={()=>this.props.goResult(item.key) }>
            <Text style={styles.item}>{item.key}</Text>
          </TouchableOpacity>}
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 22
  },
  item: {
    padding: 10,
    fontSize: 14,
    height: 44,
  },
})
