
#@ File (label = "Input directory", style = "directory") input
#@ String (label = "File suffix", value = ".png") suffix


processFolder(input);

function processFolder(input) {
	list = getFileList(input);
	list = Array.sort(list);
	for (i = 0; i < list.length; i++) {
		if(File.isDirectory(input + File.separator + list[i]))
			processFolder(input + File.separator + list[i]);
		if(endsWith(list[i], suffix))
			processFile(input, list[i]);
	}
}

function processFile(input, file) {
	inputFile =  input + File.separator + file;
			
	open(inputFile);
	
	open(getDirectory("luts") + "red_lut.lut");
	saveAs("PNG", inputFile);
	close();
	print("Saving to: " + inputFile);
}
