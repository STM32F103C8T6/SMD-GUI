import json


if __name__ == '__main__':
    User_Seting_json_path = '/mnt/E/Linux/SMD_GUI/User_Defined.json'
    Software_Default_json_path = '/mnt/E/Linux/SMD_GUI/Software_Default.json'

    Software_Default = {
        'Ligand_endswith':'.mol2',
        'protein_endswith':'.pdb',
        'Ligand_Name': 'LIG',
        'Force_Field': ['AMBER14SB_parmbsc1', 'CHARMM all-atom force field'],
        'water_model': ['TIP4P', 'TIP3P', 'SPC'],
        'N_term': ['NH3+'],
        'C_term': ['COO-'],
        'Box_shape': ['dodecahedron', 'cubic', 'octahedron'], 
        'Box_size': 10,
        'Neutralize_positive_ions': ["NA","LI","K"],
        'Neutralize_negative_ions':["CL","Br","I","F"],
        'positive_ions': ["NA","CA","LI","K","Zn","MG"],
        'negative_ions': ["CL","Br","I","F"],
        'Salt_density': 0.15,
        'EM_steps': 2000,
        'EM_rvdw': 1.2,
        'NVT_step': 50000,
        'EM_rvdw': 1.2,
        'NVT_step': 50000,
        'NVT_rvdw': 1.2,
        'NVT_Tem': 300,
        'NPT_Setps': 50000,
        'NPT_rvdw': 1.2,
        'NPT_pres': 1.0,
        'SMD_Cycle_numb': 3,
        'MD_Time': 10,
        'MD_Time_Step': 2,
        'Frame_Export': 1000,
        'Trajectory_Recording': 5000,
        'Energy_Recording': 5000,
        'MD_Cutoff_Rafius': 9
    }

    user_seting = {
        'Sob_top_PATH':'/home/sxc/nfsroot/PDBbind/sobtop_1.0',
        'CGENFF_web_URL': 'https://app.cgenff.com/login',
        'CGENFF_user_name': '20225226003@stu.suda.edu.cn',
        'CGENFF_pw': 'Sxc07224819',
        'Web_Proxy': 'http://127.0.0.1:%mixedPort%',
        'Custom_EM_mdp': '/home/sxc/Server/MolecularDynamics/PHIP_chemdiv/md_file/em.mdp',
        'NVT_mdp_file': '/home/sxc/nfsroot/PDBbind/md_file/nvt.mdp',
        'NPT_mdp_file_path': '/home/sxc/nfsroot/PDBbind/md_file/npt.mdp',
        'md_mdp_file_path': '/home/sxc/Server/MolecularDynamics/PHIP_chemdiv/md_file/md.mdp',
        "gmx_python_path": '/home/sxc/miniconda3/envs/gmx/bin/python',
        "charmm_force_file_folder_path":'/home/sxc/Server/MolecularDynamics/PHIP_chemdiv/ChemDev_purchased_list/charmm36_ljpme-jul2022.ff'
    }

    # with open(Software_Default_json_path, 'w', encoding='utf-8') as file:
    #     json.dump(Software_Default, file, ensure_ascii=False, indent=4)

    with open(User_Seting_json_path, 'w', encoding='utf-8') as file:
        json.dump(user_seting, file, ensure_ascii=False, indent=4)