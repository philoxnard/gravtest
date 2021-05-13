
"""
Written by: J. Patrick Farrell
Copyright 2019

File tools for getting information about a file, result returned in a dictionary.

"""

import datetime
import os, os.path

class FileTools():

	@staticmethod
	def getFileCreationDateTime(filePath, webPath):
		"""
		Gets the creation time of a file
		"""

		# First check if the file specified by filePath exists
		if not os.path.exists(filePath):
			return None


		file_name = os.path.basename(filePath)

		file_info = {}
		file_info["filename"] = file_name
		file_info["filepath"] = webPath

		try:
			file_datetime = datetime.datetime.fromtimestamp(os.path.getctime(filePath))

			file_info["datetime"] = file_datetime.ctime()

			file_info["size"] = os.path.getsize(filePath)

			return file_info
		except:
			print("couldn't get the file (media) datetime")
			return None

	@staticmethod
	def getFolderPath(filepath):
		"""
		Splits off the filename and gives you the folder

		Pass in a full system path of a file.
		"""

		return os.path.split( filepath )[0]

	@staticmethod
	def getFileName(filepath):
		"""
		Splits off the filename and gives you the folder

		Pass in a full system path of a file.
		"""

		return os.path.split( filepath )[1]

	@staticmethod
	def getAbsolutePath(filepath):
		"""
		Gets the absolute file path even if a partial one was passed in.
		"""

		return os.path.abspath( filepath )

	@staticmethod
	def checkAndAdjustFileName(filePath):
		"""
		This function checks for a duplicate file and increments the filename with a number
		until a filename is found that doesn't match one that is already present.

		Returns the filename of the file that is available, which if the file in filepath wasn't
		present will just be the filename in filepath that was passed in.
		"""

		if os.path.isfile(filePath) == True:
			"""There is already a file present with the same name, we need to adjust the filename
				before uploading
			"""
			basepath, file_extension = os.path.splitext(filePath)

			counter = 1
			# Set the new filename.
			file_path = basepath + "_%d" % counter + file_extension

			# Increment counter until we find a filename that is not yet present.
			while os.path.isfile(file_path) == True:
				counter = counter + 1
				file_path = basepath + "_%d" % counter + file_extension

			# The calling function only wants the filename, it already knows the path,
			#  so return it.

			basepath, file_name = os.path.split(file_path)

			return file_name
		else:
			# If not a file, just return the filename, we can use it.
			basepath, file_name = os.path.split(filePath)

			return file_name

	@staticmethod
	def checkAndAdjustFileNameForOutputFolder(inputFilePath, outputFolder, logger=None):
		"""
		This function checks for a duplicate file with the same name in the output folder
		and increments the filename with a number until a filename is found that doesn't match one that is already present.

		This function is similar to the function checkAndAdjustFileName but we are check if there is a file
		with the same name present in the output folder rather than the same folder as the inputFilePath.

		Returns the output filepath of the file that is available, which if the file name is available in the outputFolder,
		we will just return the full path to the file in the output folder.
		"""

		# First we have to break the input file path apart to get the filename
		filename = FileTools.getFileName( inputFilePath )

		# Now append this
		output_file_path = outputFolder + "/" + filename

		logger.info( "checkAndAdjustFileNameForOutputFolder, output_file_path = %s" % output_file_path)

		if os.path.isfile(output_file_path) == True:
			"""There is already a file present with the same name, we need to adjust the filename
				before uploading
			"""
			basepath, file_extension = os.path.splitext(output_file_path)

			counter = 1
			# Set the new filename.
			file_path = basepath + "_%d" % counter + file_extension

			# Increment counter until we find a filename that is not yet present.
			while os.path.isfile(file_path) == True:
				counter = counter + 1
				file_path = basepath + "_%d" % counter + file_extension

			# The calling function only wants the filename, it already knows the path,
			#  so return it.

			basepath, file_name = os.path.split(file_path)

			output_file_path = outputFolder + "/" + file_name

			return output_file_path.strip()
		else:
			# If not a file, just return the full output filepath, we can use it.
			return output_file_path.strip()

	@staticmethod
	def countFilesInFolder(folderPath):
		"""
		Counts the number of files in the folder.  Returns none if folderPath is not a path.
		"""

		if os.path.isdir( folderPath ):
			file_count = len([name for name in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, name))])
			return file_count
		else:
			return None

	@staticmethod
	def readFile(filePath):
		"""
		This reads a file and returns it as a string.
		"""

		try:
			f = open( filePath, "r" )
			file_str = f.read()
			f.close()

			return file_str
		except:
			print("Failed to read file (%s)" % filePath)
			return None

	@staticmethod
	def writeFile(filePath, fileContentsString):
		"""
		This reads a file and returns it as a string.
		"""

		try:
			f = open( filePath, "w" )
			file_str = f.write( fileContentsString )
			f.close()

			return True
		except:
			print("Failed to write file (%s)" % filePath)
			return None


if __name__ == "__main__":

	file_info = FileTools.getFileCreationDateTime("")
	print(file_info)

	date_time = FileTools.getDateTimeObject(file_info["datetime"])
	print(date_time)

