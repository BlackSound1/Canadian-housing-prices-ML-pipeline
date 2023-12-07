# COMP333Project

## Setup

1. Create virtual environment for the project
2. Activate it
3. Install all dependencies in `requirements.txt`
4. Navigate to the root of this project
5. From the terminal, run `$ mage start`. Mage should now open on your browser, 
where you can see the pipeline and all of its blocks.

6. On the right hand side, navigate to the "Variables" section:

    ![img.png](readme_pics/variable1.png)
7. Create a new global variable by clicking the "+ New" button.
The variable should be called `FILES_LOCATION` and be set to the location of `COMP333_Project_Data` on your computer:

    ![img.png](readme_pics/variable2.png)

    Remember to hit "Enter" when done to save it.

Click the play button on a block to run it.

To run all blocks in Pipeline, go the "Triggers" pane from the left hand side.
Create a new Trigger of 'Schedule' type, scheduled for now and running 'once'.

Once running, can view progress by clicking on the trigger.
