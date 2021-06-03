

## Node Manager
<img src = https://github.com/kaiwen98/spacey/blob/master/images/gui%20scrnshot.png>

### Introduction
   A Node manager is set up to allow network administrators to synchronise the geographical location of the sensors in the restaurant spaces with database, which can allow the image procesor code to generate the image to reflect the istribution of occupied seats which will be relayed to the client.
  <br> You can run Spacey Admin/admin_map_creator.py to perform left click to move the cursor throughout the map, and then right click to deposit a sensor node where the cursor is. Then, you can revisit the node information by placing the cursor over a placed node. </br>
  
## Image Processor
<img src = https://github.com/kaiwen98/spacey/blob/master/Spacey%20API/Image%20Processor/images/output%20graphic/output_lol.png>

### Introduction
   The image processor imports the relevant JSON file from the node manager to initialize the map in the respectory file directory. Thereafter, any updates in status of the seats will result in changes in the color of the respective seat and a corresponding update in the map.

### FOR EGSC DEVELOPERS
   - Note that you must set your workspace to Spacey_API, so that all the relative imports will work.
   - Ensure to install requirements from requirements.txt.
   - Run the program from main.py. The window should pop up.
   - The code base is modified heavily from the <a link = "https://github.com/kaiwen98/spacey"> source repository </a>. There are some code from there that are removed for neatness, or if I deem it to be superfluos. If somehow there's some bug, you may want to refer to the code.
   - As of now, DB operations are not working because the free trial I have signed up with Redis probably has expired. I think we will need to replace the storage functions with Firebase.