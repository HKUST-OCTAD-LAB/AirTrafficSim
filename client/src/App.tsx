import React from 'react';
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

import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';

import CesiumBase from './pages/CesiumBase';

const App = () => {
  return (
    <Router>
      <Box sx={{ display: 'flex'}}>
          <Drawer variant="permanent" anchor="left" sx={{ width: 200, flexShrink: 0, '& .MuiDrawer-paper': {width: 200}}}>
          <Toolbar>
            <Typography> ATC </Typography>
          </Toolbar>
          <Divider />
          <List>
            {['Dashboard', 'Airspace', 'Aircrafts'].map((text, index) => (
              <ListItem button key={text}>
                <ListItemIcon>
                  {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
                </ListItemIcon>
                <ListItemText primary={text} />
              </ListItem>
            ))}
          </List>
          </Drawer> 
        <Box component="main" sx={{ flexGrow: 1}}>
          <Switch>
            <Route path="/">
              <CesiumBase/>
            </Route>
          </Switch>  
        </Box>
      </Box>
    </Router>
  );
}

export default App;
