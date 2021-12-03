import React, { useState } from 'react';
import {BrowserRouter as Router, Switch, Route, Link} from "react-router-dom";
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Drawer from '@mui/material/Drawer';
import { createTheme, ThemeProvider} from '@mui/material/styles';

import socket from './utils/websocket';
import RealtTime from './pages/Realtime';
import Scenarios from './pages/Scenarios';

socket.on('connection', () => {
    console.log("connected");
  }
)

const App = () => {
  const [realTimeSelected, setRealTimeSelected] = useState(false);
  const [scenariosSelected, setScenariosSelected] = useState(false);

  const theme = createTheme({
    palette: {
      mode: 'dark',
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Box sx={{ display: 'flex'}}>
            <Drawer variant="permanent" anchor="left" sx={{ width: 200, flexShrink: 0, '& .MuiDrawer-paper': {width: 200}}}>
              <Toolbar>
                <Typography> ATC Simulator</Typography>
              </Toolbar>
              <Divider />
              <List>
                <ListItem>
                  <ListItemText primary={"Dashboard"} />
                </ListItem>
                <ListItem>
                  <ListItemText primary={"Real Time Simulation"}/>
                </ListItem>
                <ListItem>
                  <ListItemText primary={"Scenarios"}/>
                </ListItem>
                {/* <ListItem>
                  <ListItemText primary={"Map Editor"} />
                </ListItem>
                <ListItem>
                  <ListItemText primary={"Scenraios"} />
                </ListItem> */}
              </List>
            </Drawer> 
          <Box component="main" sx={{ flexGrow: 1}}>
            <Switch>
              <Route path="/">
                <RealtTime/>
              </Route>
            </Switch>  
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
