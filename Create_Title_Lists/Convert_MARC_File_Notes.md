# Situation
Convert_MARC_File_to_Title_List.json was started in another repository, but I realized that the beginning way of dealing with MARC and MarcEdit export to OpenRefine files was the only difference and as long as the first column was renamed to "SYS Number" the later parts would be the same. Additionally, the use of appendign the alphabet that I developed here could be used in the full program as a shortcut for sorting the subfields in the desired manner. As a result, the JSON and accompanying README have been moved here for incorporation into the full program later.

## Notes
Convert_MARC_File_to_Title_List doesn't
- deal with repeating fields or repeating subfields within a field
- has only the 020$a, 020$z, 245$a, 245$b, 245$c, 245$n, 250$a, 264$b, 264$c, 776$i, 776$z, 856$u subfields
 - Also include 020$q, 024$a, 024$2
 - For files from UXU01, also include 035$a, 710$a, 710$e, 897$a, 897$e, 856$3, 856$z
- Volume and edition info (245$n, 250$a) isn't transformed--the irregularity requires a more complex regex
- hh

## Order of Subfields
Subfields are sorted by initially appending letters then an underscore to the front of them
- 020$a -> a_020$a
- 020$z -> b_020$z
- 776$z -> c_776$z
- 020$q -> d_020$q
- 776$i -> e_776$i
- 024$a -> f_024$a
- 024$2 -> g_024$2
- 035$a -> h_035$a
- 710$a -> i_710$a
- 710$e -> j_710$e
- 897$a -> k_897$a
- 897$e -> l_897$e
- 856$u -> m_856$u
- 856$3 -> n_856$3
- 856$z -> o_856$z
- 245$c -> p_245$c
- 264$c -> q_264$c
- 264$b -> r_264$b
- 245$a -> s_245$a
- 245$b -> t_245$b
- 245$n -> u_245$n
- 250$a -> v_250$a
