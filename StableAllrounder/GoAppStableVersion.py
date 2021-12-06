import kivy
from kivy.app import App
from kivy.lang import Builder, builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import random   
Window.size = (800, 800)


class Board(Screen):
    turn = 0
    def turning(self, but):
        
        
        if but.text == "Go":
            self.turn += 1

            #CANT PASS ID AS ARGUEMNT TO TURNING()
            for id, object in self.ids.items(): #FINDING ID OUT BY LOOKING FOR INSTANCE AND CORRESPONDING KEY (ID) IN SELF.IDS
                if str(object) == str(but):
                    but_id = id


            if self.turn % 2 == 1:
                self.player = "B"
                self.opponent = "W"
                but.text = "B"
                       

            else:
                self.player = "W"
                self.opponent = "B"
                but.text = "W"

            
            
            self.change_image(but, but_id) # place stone

            groups = self.init_groups(self.get_surrounding(but_id)) # initialize groups
            groups = self.expand_groups(but_id,groups[0],groups[1],groups[2],groups[3]) #expand groups


            self.check_killing(groups, but_id) # checks if a group gets killed

    def change_image(self, but, but_id): #perhaps go through all ids and change image

        if self.player == "B": # for testing purposes # if for all ids, then check but.text property
            if but_id[3] == "1": # first row
                if but_id[2] == "1": # Top Left Corner
                    but.ids["Image"].source = "Graphics\Splitter\BlackField\TopLeftCornerBlack.png"
                
                elif but_id[2] == "9": # Top Right Corner
                    but.ids["Image"].source = "Graphics\Splitter\BlackField\TopRightCornerBlack.png"

                else: # Top Edge
                    but.ids["Image"].source = "Graphics\Splitter\BlackField\TopEdgeBlack.png"

            elif but_id[3] == "9": # last row
                if but_id[2] == "1": # Bottom Left Corner
                    but.ids["Image"].source = "Graphics\Splitter\BlackField\BottomLeftCornerBlack.png"
                
                elif but_id[2] == "9": # Bottom Right Corner
                    but.ids["Image"].source = "Graphics\Splitter\BlackField\BottomRightCornerBlack.png"

                else: # Bottom Edge
                    but.ids["Image"].source = "Graphics\Splitter\BlackField\BottomEdgeBlack.png"

            elif but_id[2] == "1": #first column/spalte #Corners have already been checked
                but.ids["Image"].source = "Graphics\Splitter\BlackField\LeftEdgeBlack.png"

            elif but_id[2] == "9": #last column/spalte #Corners have already been checked
                but.ids["Image"].source = "Graphics\Splitter\BlackField\RightEdgeBlack.png"

            else:
                but.ids["Image"].source = "Graphics\Splitter\BlackField\IntersectionBlack.png"

        elif self.player =="W":
            if but_id[3] == "1": # first row
                if but_id[2] == "1": # Top Left Corner
                    but.ids["Image"].source = "Graphics\Splitter\WhiteField\TopLeftCornerWhite.png"
                
                elif but_id[2] == "9": # Top Right Corner
                    but.ids["Image"].source = "Graphics\Splitter\WhiteField\TopRightCornerWhite.png"

                else: # Top Edge
                    but.ids["Image"].source = "Graphics\Splitter\WhiteField\TopEdgeWhite.png"

            elif but_id[3] == "9": # last row
                if but_id[2] == "1": # Bottom Left Corner
                    but.ids["Image"].source = "Graphics\Splitter\WhiteField\BottomLeftCornerWhite.png"
                
                elif but_id[2] == "9": # Bottom Right Corner
                    but.ids["Image"].source = "Graphics\Splitter\WhiteField\BottomRightCornerWhite.png"

                else: # Bottom Edge
                    but.ids["Image"].source = "Graphics\Splitter\WhiteField\BottomEdgeWhite.png"

            elif but_id[2] == "1": #first column/spalte #Corners have already been checked
                but.ids["Image"].source = "Graphics\Splitter\WhiteField\LeftEdgeWhite.png"

            elif but_id[2] == "9": #last column/spalte #Corners have already been checked
                but.ids["Image"].source = "Graphics\Splitter\WhiteField\RightEdgeWhite.png"

            else:
                but.ids["Image"].source = "Graphics\Splitter\WhiteField\IntersectionWhite.png"
        

    def test_groups(self, groups):
        for group in groups:
            if len(group) > 2 and group[0] == self.opponent:
                for stone in group[1:]:
                    self.ids[stone].ids["Image"].source = "Graphics\Splitter\Test.png"
            
    def init_groups(self, surrounding):

        # CREATES GROUPS IN SCHEME ['color', 'first ID' ] FOR EVERY DIRECTION

        surrounding_colors = list(surrounding.values())
        surrounding_ids = list(surrounding)

        north_group = []
        north_group.append(surrounding_colors[0])
        north_group.append(surrounding_ids[0])

        east_group = []
        east_group.append(surrounding_colors[1])
        east_group.append(surrounding_ids[1])

        south_group = []
        south_group.append(surrounding_colors[2])
        south_group.append(surrounding_ids[2])

        west_group = []
        west_group.append(surrounding_colors[3])
        west_group.append(surrounding_ids[3])

        groups = [north_group, east_group, south_group, west_group]

        return groups

    def expand_groups(self, but_id, north_group, east_group, south_group, west_group):
        extending = True
        
        if north_group[0] != "Edge" and north_group[0] != "Go":
            while extending:
                new_stones = []
                
                
                for stone in north_group[1:]: # you can check too if 0 not in stone to skip edges but so far no bugs no need for that 
                    surrounding = self.get_surrounding(stone)
                    #print(stone, surrounding)
                    for id, color in surrounding.items():
                        
                        if color == north_group[0] and id not in north_group and id not in new_stones: # NEW STONE
                            new_stones.append(id)
                            

                            
                if new_stones == []: # GROUP COMPLETE, NO NEW STONES FOUND
                    break

                else: # FOUND NEW STONES; ADD TO NORTH_GROUP AND REPAT SERACH
                    north_group.extend(new_stones)

        if east_group[0] != "Edge" and east_group[0] != "Go":
            while extending:
                new_stones = []
                
                
                for stone in east_group[1:]: # you can check too if 0 not in stone to skip edges but so far no bugs no need for that 
                    surrounding = self.get_surrounding(stone)

                    for id, color in surrounding.items():
                        
                        if color == east_group[0] and id not in east_group and id not in new_stones: # NEW STONE
                            new_stones.append(id)

                            
                if new_stones == []: # GROUP COMPLETE, NO NEW STONES FOUND
                    break

                else: # FOUND NEW STONES; ADD TO NORTH_GROUP AND REPAT SERACH
                    east_group.extend(new_stones)   

        if south_group[0] != "Edge" and south_group[0] != "Go":
            while extending:
                new_stones = []
                
                
                for stone in south_group[1:]: # you can check too if 0 not in stone to skip edges but so far no bugs no need for that 
                    surrounding = self.get_surrounding(stone)

                    for id, color in surrounding.items():
                        
                        if color == south_group[0] and id not in south_group and id not in new_stones: # NEW STONE
                            new_stones.append(id)

                            
                if new_stones == []: # GROUP COMPLETE, NO NEW STONES FOUND
                    break

                else: # FOUND NEW STONES; ADD TO NORTH_GROUP AND REPAT SERACH
                    south_group.extend(new_stones)         

        if west_group[0] != "Edge" and west_group[0] != "Go":
            while extending:
                new_stones = []
                
                
                for stone in west_group[1:]: # you can check too if 0 not in stone to skip edges but so far no bugs no need for that 
                    surrounding = self.get_surrounding(stone)

                    for id, color in surrounding.items():
                        
                        if color == west_group[0] and id not in west_group and id not in new_stones: # NEW STONE
                            new_stones.append(id)

                            
                if new_stones == []: # GROUP COMPLETE, NO NEW STONES FOUND
                    break

                else: # FOUND NEW STONES; ADD TO NORTH_GROUP AND REPAT SERACH
                    west_group.extend(new_stones)    

                 

        print("Move:", self.turn)
        print("north_group", north_group)
        print("east group:", east_group)
        print("south group:", south_group)
        print("west_group", west_group, "\n")

        groups = (north_group, east_group, south_group, west_group)

        return groups
        
            

    def get_surrounding(self, but_id):
        surrounding = {} # { '(north)id': 'color', '(east)id': 'color'.... }
        
        # SLICES GIVEN ID UP AND CHANGES X/Y COORDINATE
        # LOOKS AT ID.TEXT VALUE TO DETECT COLOR

        north_id = but_id[:3] + str(int(but_id[3])-1) 
        if north_id[3] == "0":
            north_color = "Edge"
        else:
            north_color = self.ids[north_id].text

        surrounding[north_id] = north_color

        east_id = but_id[:2] + str(int(but_id[2])+1) + but_id[3]
        if east_id[2:4] == "10":
            east_color = "Edge"
        else:
            east_color = self.ids[east_id].text

        surrounding[east_id] = east_color

        south_id = but_id[:3] + str(int(but_id[3])+1)
        if south_id[3:] == "10":
            south_color = "Edge"
        else:
            south_color = self.ids[south_id].text

        surrounding[south_id] = south_color

        west_id = but_id[:2] + str(int(but_id[2])-1) + but_id[3]
        if west_id[2] == "0":
            west_color = "Edge"
        else:
            west_color = self.ids[west_id].text

        surrounding[west_id] = west_color
        
        return surrounding

        # Check north south etc and write change it to B or W instead of id or use stones list
        
        
    def check_killing(self, groups, current_move): # checks if group gets killed
        murder = False
        suicide_attempt = False
        for group in groups:
            liberties = False
    
            #check whether groups are surrounded, just looks for liberties 

            if group[0] != "Edge" and group[0] != "Go": # only check groups that contain stones

                for stone in group[1:]:
                    if not liberties: # No liberties found yet
                        surrounding = self.get_surrounding(stone)
                        for id, color in surrounding.items():
                            if color == "Go":
                                liberties = True
                                break
                        
                    else: #liberties found!
                        break

                    if stone == group[len(group)-1] and not liberties: # Last stone checked, no liberties found 
                        if group[0] == self.opponent: # enemy groups gets removed
                            self.remove_stones(group) # remove stones
                            murder = True
                            

                        elif group[0] == self.player: # suicide # check only works for groups > 1
                            # ONLY SUICIDE IF NO ENEMY STONE GETS KILLED IN THE PROCESS
                            # SO EVERY GROUP HAS TO BE CHECKED FOR KILLING FIRST
                            suicide_attempt = True


        current_move_surrounding = self.get_surrounding(current_move) 
        surrounding_colors = current_move_surrounding.values()

        if not murder: #NO ENEMEY GROUPS GET KILLED
            if suicide_attempt: # player kills his own group
                self.illegal_move(current_move) # first element is current move 

            # PLAYER KILLS A SINGLE STONE
            elif self.player not in surrounding_colors and "Go" not in surrounding_colors:
                self.illegal_move(current_move)
                

    def illegal_move(self, but_id):
        # change image, text and player/opponnent count back
        print("[Illegal Move]")
        self.ids[but_id].text = "Go"
        self.turn -= 1

        dead_stone = [self.player, but_id] # get it in the group format so it can be removed by remove_stones()
        self.remove_stones(dead_stone)

                    
        
    def remove_stones(self, group):
        for stone in group[1:]: # set text and image to default
            self.ids[stone].text = "Go"
            if stone[3] == "1": # first row
                if stone[2] == "1": # Top Left Corner
                    self.ids[stone].ids["Image"].source = "Graphics\Splitter\EmptyField\TopLeftCorner.png"
                
                elif stone[2] == "9": # Top Right Corner
                    self.ids[stone].ids["Image"].source = "Graphics\Splitter\EmptyField\TopRightCorner.png"

                else: # Top Edge
                    self.ids[stone].ids["Image"].source = "Graphics\Splitter\EmptyField\TopEdge.png"

            elif stone[3] == "9": # last row
                if stone[2] == "1": # Bottom Left Corner
                    self.ids[stone].ids["Image"].source = "Graphics\Splitter\EmptyField\BottomLeftCorner.png"
                
                elif stone[2] == "9": # Bottom Right Corner
                    self.ids[stone].ids["Image"].source = "Graphics\Splitter\EmptyField\BottomRightCorner.png"

                else: # Bottom Edge
                    self.ids[stone].ids["Image"].source = "Graphics\Splitter\EmptyField\BottomEdge.png"

            elif stone[2] == "1": #first column/spalte #Corners have already been checked
                self.ids[stone].ids["Image"].source = "Graphics\Splitter\EmptyField\LeftEdge.png"

            elif stone[2] == "9": #last column/spalte #Corners have already been checked
                self.ids[stone].ids["Image"].source = "Graphics\Splitter\EmptyField\RightEdge.png"

            else:
                self.ids[stone].ids["Image"].source = "Graphics\Splitter\EmptyField\Intersection.png"



class WindowManager(ScreenManager):
    pass



class GoApp(App):
    def build(self):
        return kv

    def turning(self, but):
        id = but.text
        print(self.ids.but.text)

kv = Builder.load_file("GoAppStableKV.kv")

if __name__ == "__main__":
    GoApp().run()
