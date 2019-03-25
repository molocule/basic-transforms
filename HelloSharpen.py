import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import numpy as np
from array import array

#
# HelloSharpen
#

class HelloSharpen(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Simple Module Operations" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["Claudia, Geoff"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
Select two volumes if the operation calls for two volumes. If not, just select one, but make sure you select Volume
1. The console may ask you for inputs (scalars, etc.) 
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
No grant, knowledge is priceless
""" # replace with organization, grant and thanks.

#
# HelloSharpenWidget
#

class HelloSharpenWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """



  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "List of Operators"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # input volume selector
    #


    # input volume 1
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume1: ", self.inputSelector)
    # input volume 2
    self.inputSelector2 = slicer.qMRMLNodeComboBox()
    self.inputSelector2.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputSelector2.selectNodeUponCreation = True
    self.inputSelector2.addEnabled = False
    self.inputSelector2.removeEnabled = False
    self.inputSelector2.noneEnabled = False
    self.inputSelector2.showHidden = False
    self.inputSelector2.showChildNodeTypes = False
    self.inputSelector2.setMRMLScene( slicer.mrmlScene )
    self.inputSelector2.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume2: ", self.inputSelector2)
    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.outputSelector.selectNodeUponCreation = True
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = True
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)
    #
    # threshold value
    #
    self.imageThresholdSliderWidget = ctk.ctkSliderWidget()
    self.imageThresholdSliderWidget.singleStep = 0.1
    self.imageThresholdSliderWidget.minimum = -100
    self.imageThresholdSliderWidget.maximum = 100
    self.imageThresholdSliderWidget.value = 0.5
    self.imageThresholdSliderWidget.setToolTip("Set threshold value for computing the output image. Voxels that have intensities lower than this value will set to zero.")
    parametersFormLayout.addRow("Image threshold", self.imageThresholdSliderWidget)
    #
    # check box to trigger taking screen shots for later use in tutorials
    #
    self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    self.enableScreenshotsFlagCheckBox.checked = 0
    self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

    #
    # Different Operations
    #

    # multiplication
    self.applyButton = qt.QPushButton("Multiply")
    self.applyButton.toolTip = "Run the operator."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)
    # connections
    self.applyButton.connect('clicked(bool)', self.onApply)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputSelector2.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # division
    self.div = qt.QPushButton("Divide")
    self.div.toolTip = "Run the operator."
    self.div.enabled = False
    parametersFormLayout.addRow(self.div)
    # connections
    self.div.connect('clicked(bool)', self.onDiv)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputSelector2.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # addition
    self.add = qt.QPushButton("Add")
    self.add.toolTip = "Run the operator."
    self.add.enabled = True
    parametersFormLayout.addRow(self.add)
    # connections
    self.add.connect('clicked(bool)', self.onAdd)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputSelector2.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # exp
    self.exp = qt.QPushButton("Exponent")
    self.exp.toolTip = "Run the operator."
    self.exp.enabled = True
    parametersFormLayout.addRow(self.exp)
    # connections
    self.exp.connect('clicked(bool)', self.onExp)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)    

    # pow
    self.pow = qt.QPushButton("Raise to the Power")
    self.pow.toolTip = "Run the operator."
    self.pow.enabled = True
    parametersFormLayout.addRow(self.pow)
    # connections
    self.pow.connect('clicked(bool)', self.onPow)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)  

    # pow
    self.pow = qt.QPushButton("Raise to the Power")
    self.pow.toolTip = "Run the operator."
    self.pow.enabled = True
    parametersFormLayout.addRow(self.pow)
    # connections
    self.pow.connect('clicked(bool)', self.onPow)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)  

    # log
    self.logg = qt.QPushButton("Take Natural Log of")
    self.logg.toolTip = "Run the operator."
    self.logg.enabled = True
    parametersFormLayout.addRow(self.logg)
    # connections
    self.pow.connect('clicked(bool)', self.onLog)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)    

    # Add vertical spacer
    self.layout.addStretch(1)
    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass




# the addition operator 
  def onAdd(self):
  	m1 = self.inputSelector.currentNode()
	m2 = self.inputSelector2.currentNode()
	vn = self.outputSelector.currentNode()

	print(np.array(m1.GetName()))

	m1arr = slicer.util.array(m1.GetName())
	m2arr = slicer.util.array(m2.GetName())

	w = m1arr + m2arr

	n = slicer.util.getNode(vn.GetName())

	slicer.util.updateVolumeFromArray(n, w)

# the addition operator 
  def onPow(self):
  	m1 = self.inputSelector.currentNode()
	vn = self.outputSelector.currentNode()

	print(np.array(m1.GetName()))

	m1arr = slicer.util.array(m1.GetName())

	d = 3

	w = np.power(m1arr, d)

	n = slicer.util.getNode(vn.GetName())

	slicer.util.updateVolumeFromArray(n, w)

  def onLog(self):
  	m1 = self.inputSelector.currentNode()
	vn = self.outputSelector.currentNode()

	print(np.array(m1.GetName()))

	m1arr = slicer.util.array(m1.GetName())

	w = np.power(m1arr, d)

	n = slicer.util.getNode(vn.GetName())

	slicer.util.updateVolumeFromArray(n, w)

# the exponential operator 
  def onExp(self):
  	m1 = self.inputSelector.currentNode()
	vn = self.outputSelector.currentNode()

	print(np.array(m1.GetName()))

	m1arr = slicer.util.array(m1.GetName())

	w = np.log(m1arr)

	n = slicer.util.getNode(vn.GetName())

	slicer.util.updateVolumeFromArray(n, w)


# the multiplication operator
  def onApply(self):

# PROBLEMATIC
# please ignore the following code for taking in inputs. 
  	a, b = [raw_input("Enter a two values for scaling 1, 2 respecitvely: ").split(':')]
	print("First number is {} and second number is {}".format(a, b))
	print()

	n1 = int(a)
	n2 = int(b)

  	m1 = self.inputSelector.currentNode()
	m2 = self.inputSelector2.currentNode()
	vn = self.outputSelector.currentNode()

	print(np.array(m1.GetName()))


	m1arr = slicer.util.array(m1.GetName())
	m2arr = slicer.util.array(m2.GetName())

	w = n1 * m1arr * n2 * m2arr 

	n = slicer.util.getNode(vn.GetName())

	slicer.util.updateVolumeFromArray(n, w)

# the multiplication operator
  def onDiv(self):
  	m1 = self.inputSelector.currentNode()
	m2 = self.inputSelector2.currentNode()
	vn = self.outputSelector.currentNode()

	print(np.array(m1.GetName()))


	m1arr = slicer.util.array(m1.GetName())
	m2arr = slicer.util.array(m2.GetName())

	w = m1arr / (m2arr + 0.1)

	n = slicer.util.getNode(vn.GetName())

	slicer.util.updateVolumeFromArray(n, w)


  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.inputSelector2.currentNode() and self.outputSelector.currentNode()


class HelloSharpenLogic(ScriptedLoadableModuleLogic):

	def hasImageData(self,volumeNode):

	    if not volumeNode:
	      logging.debug('hasImageData failed: no volume node')
	      return False
	    if volumeNode.GetImageData() is None:
	      logging.debug('hasImageData failed: no image data in volume node')
	      return False
	    return True

	def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    
	    if not inputVolumeNode:
	      logging.debug('isValidInputOutputData failed: no input volume node defined')
	      return False
	    if not outputVolumeNode:
	      logging.debug('isValidInputOutputData failed: no output volume node defined')
	      return False
	    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
	      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
	      return False
	    return True

	def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
	    """
	    Run the actual algorithm
	    """

	    logging.info('Processing started')

	    # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
	    cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
	    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)

	    # Capture screenshot
	    if enableScreenshots:
	      self.takeScreenshot('HelloSharpenTest-Start','MyScreenshot',-1)

	    logging.info('Processing completed')

	    return True


class HelloSharpenTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_HelloSharpen1()

  def test_HelloSharpen1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import SampleData
    SampleData.downloadFromURL(
      nodeNames='FA',
      fileNames='FA.nrrd',
      uris='http://slicer.kitware.com/midas3/download?items=5767')
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = HelloSharpenLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
