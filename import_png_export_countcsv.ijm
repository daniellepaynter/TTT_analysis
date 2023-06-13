#@ File (label = "Input directory", style = "directory") input_big
#@ File (label = "Output directory", style = "directory") output
#@ String (label = "File suffix", value = ".png") suffix


processFolder(input_big);

function processFolder(input_big) {
	list = getFileList(input_big);
	list = Array.sort(list);
	for (i = 0; i < list.length; i++) {
		if(File.isDirectory(input_big + File.separator + list[i]))
			processFolder(input_big + File.separator + list[i]);
		if(endsWith(list[i], suffix))
			print(list[i]);
			processFile(input_big, list[i]);
	}
}
function processFile(input, file) {
	print("Processing: " + input + File.separator + file);
	inputfile = input + File.separator + file;
	csv_save = replace(file, ".png", "_fijicounts.csv");
	open( inputfile );
	selectWindow(file);
	setThreshold(0, 1);
	run("Convert to Mask");
    run("Invert LUT");
	run("Analyze Particles...", "size=45-Infinity display clear");
	saveAs("Results", output + File.separator + csv_save);
	close( file );
}
