import rospy
import pytest

import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import Image
from aruco_pose.msg import MarkerArray
from visualization_msgs.msg import MarkerArray as VisMarkerArray


@pytest.fixture
def node():
    return rospy.init_node('aruco_pose_test', anonymous=True)

@pytest.fixture
def tf_buffer():
    buf = tf2_ros.Buffer()
    tf2_ros.TransformListener(buf)
    return buf

def approx(expected):
    return pytest.approx(expected, abs=1e-4) # compare floats more roughly

def test_markers(node):
    markers = rospy.wait_for_message('aruco_detect/markers', MarkerArray, timeout=5)
    assert len(markers.markers) == 4
    assert markers.header.frame_id == 'main_camera_optical'

    assert markers.markers[0].id == 2
    assert markers.markers[0].length == approx(0.33)
    assert markers.markers[0].pose.position.x == approx(0.36706567854)
    assert markers.markers[0].pose.position.y == approx(0.290484516644)
    assert markers.markers[0].pose.position.z == approx(2.18787602301)
    assert markers.markers[0].pose.orientation.x == approx(0.993997406299)
    assert markers.markers[0].pose.orientation.y == approx(-0.00532003481626)
    assert markers.markers[0].pose.orientation.z == approx(-0.107390951553)
    assert markers.markers[0].pose.orientation.w == approx(0.0201999263402)
    assert markers.markers[0].c1.x == approx(415.557739258)
    assert markers.markers[0].c1.y == approx(335.557739258)
    assert markers.markers[0].c2.x == approx(509.442260742)
    assert markers.markers[0].c2.y == approx(335.557739258)
    assert markers.markers[0].c3.x == approx(509.442260742)
    assert markers.markers[0].c3.y == approx(429.442260742)
    assert markers.markers[0].c4.x == approx(415.557739258)
    assert markers.markers[0].c4.y == approx(429.442260742)

    assert markers.markers[3].id == 3
    assert markers.markers[3].length == approx(0.1)
    assert markers.markers[3].pose.position.x == approx(-0.1805169666)
    assert markers.markers[3].pose.position.y == approx(-0.200697302327)
    assert markers.markers[3].pose.position.z == approx(0.585767514823)
    assert markers.markers[3].pose.orientation.x == approx(-0.961738074009)
    assert markers.markers[3].pose.orientation.y == approx(-0.0375180244707)
    assert markers.markers[3].pose.orientation.z == approx(-0.0115387773672)
    assert markers.markers[3].pose.orientation.w == approx(0.271144115664)
    assert markers.markers[3].c1.x == approx(129.557723999)
    assert markers.markers[3].c1.y == approx(49.557723999)
    assert markers.markers[3].c2.x == approx(223.442276001)
    assert markers.markers[3].c2.y == approx(49.557723999)
    assert markers.markers[3].c3.x == approx(223.442276001)
    assert markers.markers[3].c3.y == approx(143.442276001)
    assert markers.markers[3].c4.x == approx(129.557723999)
    assert markers.markers[3].c4.y == approx(143.442276001)

    assert markers.markers[1].id == 1
    assert markers.markers[1].length == approx(0.33)
    assert markers.markers[2].id == 4
    assert markers.markers[2].length == approx(0.33)

def test_markers_frames(node, tf_buffer):
    marker_2 = tf_buffer.lookup_transform('main_camera_optical', 'aruco_2', rospy.Time(), rospy.Duration(5))
    assert marker_2.transform.translation.x == approx(0.36706567854)
    assert marker_2.transform.translation.y == approx(0.290484516644)
    assert marker_2.transform.translation.z == approx(2.18787602301)
    assert marker_2.transform.rotation.x == approx(0.993997406299)
    assert marker_2.transform.rotation.y == approx(-0.00532003481626)
    assert marker_2.transform.rotation.z == approx(-0.107390951553)
    assert marker_2.transform.rotation.w == approx(0.0201999263402)

def test_map_markers_frames(node, tf_buffer):
    stamp = rospy.get_rostime()
    timeout = rospy.Duration(5)

    marker_1 = tf_buffer.lookup_transform('aruco_map', 'aruco_map_1', stamp, timeout)
    assert marker_1.transform.translation.x == approx(0)
    assert marker_1.transform.translation.y == approx(0)
    assert marker_1.transform.translation.z == approx(0)

    marker_4 = tf_buffer.lookup_transform('aruco_map', 'aruco_map_4', stamp, timeout)
    assert marker_4.transform.translation.x == approx(1)
    assert marker_4.transform.translation.y == approx(1)
    assert marker_4.transform.translation.z == approx(0)

    marker_12 = tf_buffer.lookup_transform('aruco_map', 'aruco_map_12', stamp, timeout)
    assert marker_12.transform.translation.x == approx(0.2)
    assert marker_12.transform.translation.y == approx(0.5)
    assert marker_12.transform.translation.z == approx(0)

def test_visualization(node):
    vis = rospy.wait_for_message('aruco_detect/visualization', VisMarkerArray, timeout=5)
    assert len(vis.markers) == 9

def test_debug(node):
    img = rospy.wait_for_message('aruco_detect/debug', Image, timeout=5)
    assert img.width == 640
    assert img.height == 480
    assert img.header.frame_id == 'main_camera_optical'

def test_map(node):
    pose = rospy.wait_for_message('aruco_map/pose', PoseWithCovarianceStamped, timeout=5)
    assert pose.header.frame_id == 'main_camera_optical'
    assert pose.pose.pose.position.x == approx(-0.629167753342)
    assert pose.pose.pose.position.y == approx(0.293822650809)
    assert pose.pose.pose.position.z == approx(2.12641343155)
    assert pose.pose.pose.orientation.x == approx(-0.998383794799)
    assert pose.pose.pose.orientation.y == approx(-5.20919098575e-06)
    assert pose.pose.pose.orientation.z == approx(-0.0300861070302)
    assert pose.pose.pose.orientation.w == approx(0.0482143590507)

def test_map_image(node):
    img = rospy.wait_for_message('aruco_map/image', Image, timeout=5)
    assert img.width == 2000
    assert img.height == 2000
    assert img.encoding == 'mono8'

def test_map_visualization(node):
    vis = rospy.wait_for_message('aruco_map/visualization', VisMarkerArray, timeout=5)

def test_map_debug(node):
    img = rospy.wait_for_message('aruco_map/debug', Image, timeout=5)
