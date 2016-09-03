#include "image_feature.hpp"

#include <map>
#include <string>
#include <utility>
#include <vector>

#include "jubatus/util/data/string/utility.h"
#include "jubatus/core/fv_converter/exception.hpp"
#include "jubatus/core/fv_converter/util.hpp"


namespace jubatus {
namespace plugin {
namespace fv_converter {

image_feature::image_feature(
	float mrate,
	const std::string& algorithm)
	: mrate_(mrate),
	  algorithm_(algorithm){
	//some exceptions
}

void image_feature::add_feature(
	const std::string& key,
	const std::string& value,
	std::vector<std::pair<std::string,float> >& ret_fv) const{
	std::vector<unsigned char> buf(value.begin(), value.end());
	cv::Mat mat_orig = cv::imdecode(cv::Mat(buf), CV_LOAD_IMAGE_COLOR);
	// resize img
	cv::Mat mat;
	cv::resize(mat_orig, mat, cv::Size(),mrate_,mrate_);
	cv::Mat grayImage;
	cv::cvtColor(mat, grayImage, CV_BGR2GRAY);
	
	if (algorithm_ == "RGB"){
		// std::cout << algorithm_ << std::endl;
		for (int y = 0; y < mat.rows; ++y) {
			for (int x = 0; x < mat.cols; ++x) {
				const cv::Vec3b& vec = mat.at<cv::Vec3b>(y, x);
				for (int c = 0; c < 3; ++c) {
					std::ostringstream oss;
					oss << key << '-' << x << '-' << y << '-' << c;
					float val = static_cast<float>(vec[c]) / 255.0;
					ret_fv.push_back(std::make_pair(oss.str(), val));
				}
			}
		}
	}
	else if (algorithm_ == "DENSE"){
		// std::cout << algorithm_ << std::endl;
		// decide pixel sizes
		cv::Mat mat_resize;
		float size_x = 28.0;
		float size_y = 28.0;
		float m_x = size_x / mat_orig.cols;
		float m_y = size_y / mat_orig.rows;
		cv::resize(mat_orig, mat_resize, cv::Size(), m_x , m_y);
		
		// to gray scale
		cv::Mat mat_gray;
		// cv::cvtColor(mat_resize, mat_gray, CV_BGR2GRAY); 
		cv::cvtColor(mat_resize, mat_gray, CV_BGR2GRAY); 
		// dense key point
		std::vector<cv::KeyPoint> kp_vec;
		int step = 1;
		for (int y=step; y<mat_gray.rows-step; y+=step){
			for (int x=step; x<mat_gray.cols-step; x+=step){
				kp_vec.push_back(cv::KeyPoint(float(x),float(y),float(step)));
			}
		}

		cv::Ptr<cv::Feature2D> extractor = cv::ORB::create(500,1.2f,8,12,0,2,0,31);
		// cv::Ptr<cv::Feature2D> extractor = cv::BRISK::create();
		cv::Mat descriptors;
	    extractor->compute(mat_gray, kp_vec, descriptors);
		
		// cv::Ptr<cv::Feature2D> akaze = cv::AKAZE::create();
		// std::vector<cv::KeyPoint> key_akaze;
		// akaze->detect(mat_gray,key_akaze);
		// std::cout << key_akaze.size() <<  " keypoints are detected" << std::endl;
		// cv::Mat descriptors;
		// akaze->compute(mat_gray,key_akaze,descriptors);


	    // *logs
		// std::cout << "keypoints of img: " << kp_vec.size() << std::endl;
	    // std::cout << "x_ori "<< mat_orig.cols <<",y_ori " << mat_orig.rows <<std::endl;
		// std::cout << "m_x "<< m_x <<",m_y " << m_y <<std::endl;
	    // std::cout << "x_res "<< mat_resize.cols <<",y_res " << mat_resize.rows <<std::endl;
	    // std::cout << "descriptors of img: " << descriptors.size() << std::endl;

	    for (int i = 0; i < descriptors.rows; ++i){
	    	for (int j = 0; j < descriptors.cols; ++j){
				std::ostringstream oss;
				int p = descriptors.at<uchar>(i,j);
				oss << key << "-"<< i << "-" << j << "-" << p ;
				ret_fv.push_back(std::make_pair(oss.str(),p));
			}    	
		}
	}else{
		throw JUBATUS_EXCEPTION(
	        converter_exception("input algorithm among these ... RGB, ORB, BRISK"));
	}

}
}  // namespace fv_converter
}  // namespace plugin
}  // namespace jubatus

extern "C" {
jubatus::plugin::fv_converter::image_feature* create(
		const std::map<std::string, std::string>& params) {
	using jubatus::util::lang::lexical_cast;
	using jubatus::core::fv_converter::get_with_default;
	
	float mrate = lexical_cast<float>(get_with_default(params,"mrate","1.0"));	
	std::string algorithm = get_with_default(params,"algorithm","RGB");
	
	return new jubatus::plugin::fv_converter::image_feature(
		mrate, algorithm);
}
std::string version(){
	return "1.0";
}

} //extern "C"
