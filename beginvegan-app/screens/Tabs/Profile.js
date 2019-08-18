import React from "react";
import styled from "styled-components";

const View = styled.View`
  justify-content: center;
  align-items: center;
  flex: 1;
`;

const Text = styled.Text`
  color: white
`;

export default () => (
  <View>
    <Text>List</Text>

  </View>
);