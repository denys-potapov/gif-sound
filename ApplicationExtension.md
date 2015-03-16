# Introduction #

Add your content here.


# Details #

Add your content here.  Format your content with:
  * Text in **bold** or _italic_
  * Headings, paragraphs, and lists
  * Automatic links to other wiki pages

http://www.w3.org/Graphics/GIF/spec-gif89a.txt

26. Application Extension.

> a. Description. The Application Extension contains application-specific
> information; it conforms with the extension block syntax, as described
> below, and its block label is 0xFF.

> b. Required Version.  89a.


> c. Syntax.

> 7 6 5 4 3 2 1 0        Field Name                    Type
> +---------------+
> 0  |               |       Extension Introducer          Byte
> > +---------------+
  1. |               |       Extension Label               Byte
> > +---------------+


> +---------------+
> 0  |               |       Block Size                    Byte
> > +---------------+
  1. |               |
> > +-             -+

> 2  |               |
> > +-             -+

> 3  |               |       Application Identifier        8 Bytes
> > +-             -+

> 4  |               |
> > +-             -+

> 5  |               |
> > +-             -+

> 6  |               |
> > +-             -+

> 7  |               |
> > +-             -+

> 8  |               |
> > +---------------+

> 9  |               |
> > +-             -+
  1. |               |       Appl. Authentication Code     3 Bytes
> > +-             -+
  1. |               |
> > +---------------+


> +===============+
> |               |
> |               |       Application Data              Data Sub-blocks
> |               |
> |               |
> +===============+

> +---------------+
> 0  |               |       Block Terminator              Byte
> > +---------------+


> i) Extension Introducer - Defines this block as an extension. This
> field contains the fixed value 0x21.

> ii) Application Extension Label - Identifies the block as an
> Application Extension. This field contains the fixed value 0xFF.

> iii) Block Size - Number of bytes in this extension block,
> following the Block Size field, up to but not including the
> beginning of the Application Data. This field contains the fixed
> value 11.


> iv) Application Identifier - Sequence of eight printable ASCII
> characters used to identify the application owning the Application
> Extension.

> v) Application Authentication Code - Sequence of three bytes used
> to authenticate the Application Identifier. An Application program
> may use an algorithm to compute a binary code that uniquely
> identifies it as the application owning the Application Extension.

> Block Terminator   this field  contains the fixed value 0x00.