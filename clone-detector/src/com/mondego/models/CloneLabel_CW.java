package com.mondego.models;

public class CloneLabel_CW {
    String filePathOne;
    int startLineOne;
    int endLineOne;
    
    String filePathTwo;
    int startLineTwo;
    int endLineTwo;
    
    public CloneLabel_CW(String rawLine){
        String[] parts = rawLine.split(",");
        if (parts.length==6){
            this.filePathOne = parts[0];
            this.startLineOne = Integer.parseInt(parts[1]);
            this.endLineOne = Integer.parseInt(parts[2]);
            
            this.filePathTwo = parts[3];
            this.startLineTwo = Integer.parseInt(parts[4]);
            this.endLineTwo = Integer.parseInt(parts[5]);
        }
    }

    /**
     * @param filePathOne
     * @param startLineOne
     * @param endLineOne
     * @param filePathTwo
     * @param startLineTwo
     * @param endLineTwo
     */
    public CloneLabel_CW(String filePathOne, int startLineOne, int endLineOne,
            String filePathTwo, int startLineTwo, int endLineTwo) {
        super();
        this.filePathOne = filePathOne;
        this.startLineOne = startLineOne;
        this.endLineOne = endLineOne;
        this.filePathTwo = filePathTwo;
        this.startLineTwo = startLineTwo;
        this.endLineTwo = endLineTwo;
    }

    /* (non-Javadoc)
     * @see java.lang.Object#hashCode()
     */
    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + endLineOne;
        result = prime * result + endLineTwo;
        result = prime * result
                + ((filePathOne == null) ? 0 : filePathOne.hashCode());
        result = prime * result
                + ((filePathTwo == null) ? 0 : filePathTwo.hashCode());
        result = prime * result + startLineOne;
        result = prime * result + startLineTwo;
        return result;
    }

    /* (non-Javadoc)
     * @see java.lang.Object#equals(java.lang.Object)
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (!(obj instanceof CloneLabel_CW)) {
            return false;
        }
        CloneLabel_CW other = (CloneLabel_CW) obj;
        if (endLineOne != other.endLineOne) {
            return false;
        }
        if (endLineTwo != other.endLineTwo) {
            return false;
        }
        if (filePathOne == null) {
            if (other.filePathOne != null) {
                return false;
            }
        } else if (!filePathOne.equals(other.filePathOne)) {
            return false;
        }
        if (filePathTwo == null) {
            if (other.filePathTwo != null) {
                return false;
            }
        } else if (!filePathTwo.equals(other.filePathTwo)) {
            return false;
        }
        if (startLineOne != other.startLineOne) {
            return false;
        }
        if (startLineTwo != other.startLineTwo) {
            return false;
        }
        return true;
    }
    
    

}
